from selenium.common import TimeoutException, WebDriverException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from bs4 import BeautifulSoup
import requests

from typing import Union, List, Tuple
import time

from squidwork.actions.smtpc import SMTPController

class Actions:
    def __init__(self, browser, logger):
        self.browser = browser
        self.logger = logger
    
    def close(self):
        self.browser.close()

    def anyExpectedCondition(self, *cons):
        # hack for OR clause for expected_conditions
        return any(con(self.browser) for con in cons if self.tryCondition(con))

    def tryCondition(self, con):
        try:
            return con(self.browser)
        except Exception:
            return False
        
    def scrollByY(self, y: int):
        scroll_origin = ScrollOrigin.from_viewport(10, 10)
        ActionChains(self.browser)\
            .scroll_from_origin(scroll_origin, 0, y)\
            .perform()

    def wait(self, by_value: Tuple[str, str], timeout:float=4):
        try:
            return WebDriverWait(self.browser, timeout).until(
                expected_conditions.presence_of_element_located(by_value)
            )
        except TimeoutException:
            self.logger.error(f'Timeout: {by_value[0]} not found by {by_value[1]}')

    def click(self, by_value: Tuple[str, str], timeout:float=4, slow:Tuple[bool, float]=(False, 1)):
        time.sleep(0.1)
        by = "css_selector" if by_value[0] == "css" else by_value[0]
        by = "class_name" if by_value[0] == "class" else by_value[0]
        by_value = (getattr(By, by.upper()), by_value[1])
        try:
            element = self.wait(by_value, timeout)
            actions = ActionChains(self.browser).move_to_element(element)
            actions.pause(slow[1]) if slow[0] else None
            actions.click().perform()
            self.logger.info(f"buttonClickBy{by_value[0]}{'Slow' if slow else ''} clicked {by_value[1]}")
        except WebDriverException as e:
            self.logger.error(f"WebDriverException: {e}")

    def sendKeys(self, by_value:Tuple[str,str], keys:str, send=False,timeout:float=4):
        time.sleep(0.1)
        by = "css_selector" if by_value[0] == "css" else by_value[0]
        by = "class_name" if by_value[0] == "class" else by_value[0]
        by_value = (getattr(By, by.upper()), by_value[1])
        try:
            elem = self.wait(by_value, timeout)
            actions = ActionChains(self.browser).move_to_element(elem).pause(1)
            actions.click().perform()
            elem.clear()
            elem.send_keys(keys)
            if send:
              elem.send_keys("\n")
            self.logger.info(f"sendKeysBy{by_value[0]} sent keys to {by_value[1]}")
        except WebDriverException as e:
            self.logger.error(f"WebDriverException: {e}")

    def waitByPageURL(self, url, timeout=30):
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        title = soup.title.string if soup.title else ""
        if title:
            try:
                WebDriverWait(self.browser, timeout).until(expected_conditions.title_is(title))
                self.logger.info(f"waitByPage found {title} in page")
            except WebDriverException as e:
                self.logger.error(f"WebDriverException: {e}")

    def elementHasClass(self, element, class_name):
        try:
            ret = class_name in element.get_attribute("class")
            self.logger.info(f"Found {class_name} in {element}")
            return ret
        except WebDriverException as e:
            self.logger.error(f"WebDriverException: {e}")

    def getURL(self, url: str):
        try:
            self.browser.get(url)
            self.logger.info(f"Successfully fetched {url}")
            self.waitByPageURL(url)
        except WebDriverException as e:
            self.logger.error(f"WebDriverException: {e}")

    def request(self, url, method="GET",**kwargs):
        try:
            if method.upper() == "GET":
                return requests.get(url, **kwargs)
            if method.upper() == "POST":
                return requests.post(url, **kwargs)
        except WebDriverException as e:
            self.logger.error(f"WebDriverException: {e}")

    def sendEmail(self, to: Union[List, str], subject: str, content: str):
        try:
            mailc = SMTPController()
            mail_log = mailc.send(to=to, subject=subject, content=content)
            del mailc
            self.logger.info(mail_log)
        except WebDriverException as e:
            self.logger.error(f"WebDriverException: {e}")
