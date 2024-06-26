from selenium.common import TimeoutException, WebDriverException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys

from bs4 import BeautifulSoup
import requests

from typing import Tuple
import time

from squidwork.actions.browser.cookies import Cookies

class Browser:
    def __init__(self, driver, logger, cache_dir):
      self.driver = driver
      self.logger = logger
      self.cache_dir = cache_dir
      self.cookies = Cookies(self.cache_dir, self.logger, self.driver)

    def close(self):
        self.driver.close()

    # hack for 'or' clause for expected_conditions
    def any_expected_condition(self, *cons):
        return any(con(self.driver) for con in cons if self.try_condition(con))
    def try_condition(self, con):
        try:
            yield con(self.driver)
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
            self.driver.execute_script(f"window.scrollBy({x}, {y});")
            self.logger.info(f"actions.py:77 - Scrolled by {x}, {y}")
        except WebDriverException as e:
            self.logger.error(f"actions.py:77 - WebDriverException: {e}")
    def scroll_to(self, element):
        try:
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            self.logger.info(f"Scrolled to {element}")
        except WebDriverException as e:
            self.logger.error(f"actions.py:83 - WebDriverException: {e}")
    def scroll(self, n:int=1):
        try:
            for _ in range(n):
                body = self.driver.find_element(By.TAG_NAME, 'body')
                body.send_keys(Keys.PAGE_DOWN)
            self.logger.info(f"Scrolled {n} times")
        except WebDriverException as e:
            self.logger.error(f"actions.py:91 - WebDriverException: {e}")

    def wait(self, by_value: Tuple[str, str], timeout:float=8.0):
        try:
            return WebDriverWait(self.driver, timeout).until(
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
            actions = ActionChains(self.driver).move_to_element(element)
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
            actions = ActionChains(self.driver).move_to_element(element).pause(1)
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
                WebDriverWait(self.driver, timeout).until(expected_conditions.title_is(title))
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

    def get(self, url: str):
        try:
            self.driver.get(url)
            self.logger.info(f"Successfully fetched {url}")
            self.wait_by_page_url(url)
        except WebDriverException as e:
            self.logger.error(f"actions.py:163 - WebDriverException: {e}")

