from selenium.common import TimeoutException, WebDriverException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from bs4 import BeautifulSoup
from contextlib import contextmanager
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

    def anyExpectedCondition(self, *cons) -> bool:
        # hack for OR clause for expected_conditions, pretty nifty ngl
        return any(con(self.browser) for con in cons if self.tryCondition(con))

    def tryCondition(self, con):
        try:
            yield con(self.browser)
        except Exception:
            yield False
        finally:
            yield False
        
    def scrollByY(self, y: int) -> int:
        try:
            scroll_origin = ScrollOrigin.from_viewport(10, 10)
            ActionChains(self.browser)\
                .scroll_from_origin(scroll_origin, 0, y)\
                .perform()
            # is this better?
            # self.browser.execute_script(f"window.scrollTo(0, {y});") 
            self.logger.info(f"scrollByY scrolled to {y}")
            return 0
        except WebDriverException as e:
            self.logger.error(f"WebDriverException: {e}")
            return 1

        

    @contextmanager
    def wait(self, by_value: Tuple[str, str], timeout:float=4):
        try:
            yield WebDriverWait(self.browser, timeout).until(
                expected_conditions.presence_of_element_located(by_value)
            )
        except TimeoutException:
            self.logger.error(f'Timeout: {by_value[0]} not found by {by_value[1]}')
            yield None

    def click(self, by_value: Tuple[str, str], timeout:float=4, slow:Tuple[bool, float]=(False, 1)) -> int:
        time.sleep(0.1)
        by = "css_selector" if by_value[0] == "css" else by_value[0]
        by = "class_name" if by_value[0] == "class" else by_value[0]
        by_value = (getattr(By, by.upper()), by_value[1])
        try:
            if element := self.wait(by_value, timeout):
                actions = ActionChains(self.browser).move_to_element(element)
                actions.pause(slow[1]) if slow[0] else None
                actions.click().perform()
                self.logger.info(f"buttonClickBy{by_value[0]}{'Slow' if slow else ''} clicked {by_value[1]}")
                return 0
            else:
                return 1
        except WebDriverException as e:
            self.logger.error(f"WebDriverException: {e}")
            return 2

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

    def waitByPageURL(self, url:str, timeout:float=10.0) -> int:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        title = soup.title.string if soup.title else ""
        if title:
            try:
                WebDriverWait(self.browser, timeout).until(expected_conditions.title_is(title))
                self.logger.info(f"waitByPage found {title} in page")
                return 0
            except WebDriverException as e:
                self.logger.error(f"WebDriverException: {e}")
                return 1

    def elementHasClass(self, element, class_name) -> bool:
        try:
            if class_name in element.get_attribute("class"):
                self.logger.info(f"Found {class_name} in {element}")
                return True
        except WebDriverException as e:
            self.logger.error(f"WebDriverException: {e}")
            return False

    def getURL(self, url: str) -> int:
        try:
            self.browser.get(url)
            self.logger.info(f"Successfully fetched {url}")
            self.waitByPageURL(url)
            return 0
        except WebDriverException as e:
            self.logger.error(f"WebDriverException: {e}")
            return 1

    def request(self, url, method="GET",**kwargs) -> str:
        try:
            if method.upper() == "GET":
                return str(requests.get(url, **kwargs))
            if method.upper() == "POST":
                return str(requests.post(url, **kwargs))
        except WebDriverException as e:
            self.logger.error(f"WebDriverException: {e}")
            return ""

    def sendEmail(self, to: Union[List, str], subject: str, content: str) -> int:
        try:
            mailc = SMTPController()
            mail_log = mailc.send(to=to, subject=subject, content=content); del mailc
            self.logger.info(f"Successfully sent email:\n {mail_log}")
            return 0
        except WebDriverException as e:
            self.logger.error(f"WebDriverException: {e}")
            return 1
