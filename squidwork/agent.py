import threading, os, time
from pathlib import Path
import requests

from squidwork.driver.default_chrome_driver import DefaultChromeDriver
from squidwork.driver.driver import Driver
from squidwork.actions.actions import Actions
from squidwork.logger.logger_factory import LoggerFactory
class Agent:
    INIT_URL = "http://www.example.com/"

    def __init__(self, log_output="stdout"):
        self.cache_dir = os.path.join(os.path.expanduser("~/.cache"),  "squidwork")
        os.makedirs(self.cache_dir, exist_ok=True)
        self.logger = LoggerFactory(log_output=log_output)()
        self.browser = self.init_browser()
        self.actions = self.init_actions()
        # TODO: read from batch file or single string target #2
        # TODO: fix this load from ~/.cache/squidwork/data #1
        self.session = requests.Session()

    def __call__(self):
        self.openBrowser()
        time.sleep(0.1)
        
    def init_actions(self) -> Actions:
        user_email_creds = dict()
        user_email_creds["user_email"] = os.getenv("USER_EMAIL", None)
        user_email_creds["user_email_password"] = os.getenv("USER_EMAIL_PASSWORD", None)
        return Actions(self.browser, self.logger, user_email_creds=user_email_creds)
    
    def init_browser(self) -> Driver:
        driver_flags = dict()
        headless = True if os.getenv("HEADLESS", "0") == "1" else False
        driver_flags["headless"] = headless
        incognito = True if os.getenv("INCOGNITO", "0") == "1" else False
        driver_flags["incognito"] = incognito
        return DefaultChromeDriver(cache_dir=self.cache_dir, driver_flags=driver_flags).getBrowser()
        
    # TODO: we investigate #1
    def addCookiesToSession(self):
        try:
            # TODO: implement this #1
            cookies = self.browser.get_cookies()
        except AttributeError:
            return 1
        [
            self.session.cookies.set_cookie(
                requests.cookies.create_cookie(
                    domain=cookie["domain"],
                    name=cookie["name"],
                    value=cookie["value"],
                )
            )
            for cookie in cookies
        ]

    def openBrowser(self):
        self.addCookiesToSession()
        threading.Thread(target=self.actions.get_url(self.INIT_URL)).start()
        self.logger.info(f"Successfully opened browser")

