from selenium.common import TimeoutException, WebDriverException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from bs4 import BeautifulSoup
import requests

class Actions:
    def __init__(self, browser, logger):
        self.browser = browser
        self.logger = logger
        return None
    
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
        
    def scrollByY(self, y):
        scroll_origin = ScrollOrigin.from_viewport(10, 10)
        ActionChains(self.browser)\
            .scroll_from_origin(scroll_origin, 0, y)\
            .perform()

    def wait(self, by, value, timeout=3):
        try:
            return WebDriverWait(self.browser, timeout).until(
                expected_conditions.presence_of_element_located((getattr(By, by.upper()), value))
            )
        except TimeoutException:
            self.logger.error(f'[x] Timeout: {value} not found by {by}')

    def click(self, by, value, timeout=10, slow=False):
        if by == "css":
            by = "css_selector"
        try:
            element = self.wait(by, value, timeout)
            actions = ActionChains(self.browser).move_to_element(element)
            if slow:
                actions.pause(1)
            actions.click().perform()
            self.logger.info(f"[!] buttonClickBy{by}{'Slow' if slow else ''} clicked {value}")
        except WebDriverException as e:
            self.logger.error(f"[x] WebDriverException: {e}")

    def sendKeys(self, by, value, keys, timeout=10):
        if by == "css":
            by = "css_selector"
        try:
            elem = self.wait(by, value, timeout)
            actions = ActionChains(self.browser).move_to_element(elem).pause(1)
            actions.click().perform()
            elem.clear()
            elem.send_keys(keys)
            self.logger.info(f"[!] sendKeysBy{by} sent keys to {value}")
        except WebDriverException as e:
            self.logger.error(f"[x] WebDriverException: {e}")

    def waitByPageURL(self, url, timeout=30):
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        title = soup.title.string if soup.title else ""
        if title:
            try:
                WebDriverWait(self.browser, timeout).until(expected_conditions.title_is(title))
                self.logger.info(f"[!] waitByPage found {title} in page")
            except WebDriverException as e:
                self.logger.error(f"[x] WebDriverException: {e}")

    def elementHasClass(self, element, class_name):
        try:
            ret = class_name in element.get_attribute("class")
            self.logger.info(f"[!] Found {class_name} in {element}")
            return ret
        except WebDriverException as e:
            self.logger.error(f"[x] WebDriverException: {e}")

    def getURL(self, url):
        try:
            self.browser.get(url)
            self.logger.info(f"[!] Successfully fetched {url}")
            self.waitByPageURL(url)
        except WebDriverException as e:
            self.logger.error(f"[x] WebDriverException\n{e}")

    def request(self, url, method="GET",**kwargs):
        try:
            if method.upper() == "GET":
                return requests.get(url, **kwargs)
            if method.upper() == "POST":
                return requests.post(url, **kwargs)
        except WebDriverException as e:
            self.logger.error(f"[x] WebDriverException: {e}")