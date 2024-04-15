from selenium.common import TimeoutException, WebDriverException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from selenium.webdriver.common.keys import Keys

from bs4 import BeautifulSoup
import requests
from requests.exceptions import RequestException

from typing import Union, List, Tuple, Dict
import time

from squidwork.actions.protocols.smtpc import GmailController
from squidwork.cookies.cookies import Cookies

class Actions:
    def __init__(self, browser, logger, cache_dir, user_email_creds:Dict[str,str]=None):
        self.cache_dir = cache_dir
        self.browser = browser
        self.logger = logger
        self.user_email = user_email_creds["user_email"] 
        self.user_email_password = user_email_creds["user_email_password"] 
        self.cookies = Cookies(self.cache_dir, self.logger, self.browser)

    def close(self):
        self.browser.close()

    def get_cookies(self): return self.cookies.get_cookies()
    def import_cookies(self, filename="cookies.pkl"): return self.cookies.import_cookies(filename)
    def export_cookies(self, filename="cookies.pkl"): return self.cookies.export_cookies(filename)

    # hack for 'or' clause for expected_conditions
    def any_expected_condition(self, *cons):
        return any(con(self.browser) for con in cons if self.try_condition(con))
    def try_condition(self, con):
        try:
            yield con(self.browser)
        except Exception:
            yield False
        finally:
            yield False

    # TODO: untested
    def moveTo(self, id:str):
        element = self.driver.find_element_by_id(id)  # Replace with your element's ID
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()

    # TODO: untested
    # def smartScroll(self, element):
    #     import time
    #     scroll_pause_time = 1  # You can set your own pause time
    #     screen_height = driver.execute_script("return window.screen.height;")
    #     i = 1

    #     while True:
    #         # Scroll one screen height each time
    #         driver.execute_script(f"window.scrollTo(0, {screen_height}*{i});")
    #         i += 1
    #         time.sleep(scroll_pause_time)
    #         # Update scroll height each time after scrolling, since the page can load content
    #         scroll_height = driver.execute_script("return document.body.scrollHeight;")
    #         if (screen_height * i) > scroll_height:
    #             break  # Exit the loop when the bottom of the page is reached

    # TODO: this is broken btw fix it later
    def scroll_by(self, x:int=0, y:int=0):
        # iframe = driver.find_element_by_id('iframe-id')  # Replace with the iframe's ID
        # driver.switch_to.frame(iframe)
        try:
            self.browser.execute_script(f"window.scrollBy({x}, {y});")
            self.logger.info(f"actions.py:77 - Scrolled by {x}, {y}")
        except WebDriverException as e:
            self.logger.error(f"actions.py:77 - WebDriverException: {e}")
    def scroll_to(self, element):
        try:
            self.browser.execute_script("arguments[0].scrollIntoView(true);", element)
            self.logger.info(f"Scrolled to {element}")
        except WebDriverException as e:
            self.logger.error(f"actions.py:83 - WebDriverException: {e}")
    def scroll(self, n:int=1):
        try:
            for _ in range(n):
                body = self.browser.find_element(By.TAG_NAME, 'body')
                body.send_keys(Keys.PAGE_DOWN)
            self.logger.info(f"Scrolled {n} times")
        except WebDriverException as e:
            self.logger.error(f"actions.py:91 - WebDriverException: {e}")

    def wait(self, by_value: Tuple[str, str], timeout:float=8.0):
        try:
            return WebDriverWait(self.browser, timeout).until(
                expected_conditions.presence_of_element_located(by_value)
            )
        except TimeoutException:
            self.logger.error(f'actions.py:99 - Timeout: {by_value[0]} not found by {by_value[1]}')
            return None

    # this two can probly be shorter
    def click(self, by_value: Tuple[str, str], timeout:float=4.0, slow:Tuple[bool, float]=(False, 1)):
        time.sleep(0.1)
        by = by_value[0]
        by = "css_selector" if by_value[0] == "css" else by_value[0]
        by = "class_name" if by_value[0] == "class" else by_value[0]
        by_value = (getattr(By, by.upper()), by_value[1])
        try:
            element = self.wait(by_value, timeout)
            if element is None: return 2
            #assert element is not None, f"Element not found: {by_value[0]}: {by_value[1]}"
            actions = ActionChains(self.browser).move_to_element(element)
            actions.pause(slow[1]) if slow[0] else None
            actions.click().perform()
            self.logger.info(f"buttonClickBy{by_value[0]}{'Slow' if slow else ''} clicked {by_value[1]}")
            return 0
        except WebDriverException as e:
            self.logger.error(f"actions.py:118 - WebDriverException: {e}")
            return 1

    def type(self, by_value:Tuple[str,str], keys:str, send=False,timeout:float=4.0):
        time.sleep(0.1)
        by = "css_selector" if by_value[0] == "css" else by_value[0]
        by = "class_name" if by_value[0] == "class" else by_value[0]
        by_value = (getattr(By, by.upper()), by_value[1])
        try:
            element = self.wait(by_value, timeout)
            #assert element is not None, f"Element not found: {by_value[0]}: {by_value[1]}"
            if element is None: return 2
            actions = ActionChains(self.browser).move_to_element(element).pause(1)
            actions.click().perform()
            element.clear()
            element.send_keys(keys)
            if send:
              element.send_keys(Keys.RETURN)
            self.logger.info(f"sendKeysBy{by_value[0]} sent keys to {by_value[1]}")
            return 0
        except WebDriverException as e:
            self.logger.error(f"actions.py:136 - WebDriverException: {e}")
            return 1

    def wait_by_page_url(self, url:str, timeout:float=8.0):
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        title = soup.title.string if soup.title else ""
        if title:
            try:
                WebDriverWait(self.browser, timeout).until(expected_conditions.title_is(title))
                self.logger.info(f"waitByPage found {title} in page")
            except WebDriverException as e:
                self.logger.error(f"actions.py:147 - WebDriverException: {e}")

    def element_has_class(self, element, class_name:str):
        try:
            ret = class_name in element.get_attribute("class")
            self.logger.info(f"Found {class_name} in {element}")
            return ret
        except WebDriverException as e:
            self.logger.error(f"actions.py:155 - WebDriverException: {e}")

    def get_url(self, url: str):
        try:
            self.browser.get(url)
            self.logger.info(f"Successfully fetched {url}")
            self.wait_by_page_url(url)
        except WebDriverException as e:
            self.logger.error(f"actions.py:163 - WebDriverException: {e}")

    def request(self, url:str, method:str="GET", **kwargs) -> requests.Response:
        try:
            response = None
            if method.upper() == "GET": response = requests.get(url, **kwargs)
            elif method.upper() == "POST":response = requests.post(url, **kwargs)
            if response and response.ok: 
                return response
            else:
                self.logger.error(f"Request failed with status code: {response.status_code}")
                return None
        except RequestException as e:
            self.logger.error(f"actions.py:176 - RequestException: {e}")
            return None
        
    def send_email(self, to: Union[List, str], subject: str, content: str, provider:str="gmail"):
        try:
            assert self.user_email and self.user_email_password, "Email credentials not defined in environment variables"
            if provider.lower() == "gmail":
                mailc = GmailController(self.user_email, self.user_email_password)
            else:
                raise Exception("Provider not supported")    
            mail_log = mailc.send(to=to, subject=subject, content=content)
            # TODO: is this needed? 
            # del mailc
            self.logger.info(mail_log)
        except WebDriverException as e:
            self.logger.error(f"actioms.py:191 - WebDriverException: {e}")
