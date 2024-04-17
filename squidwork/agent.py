import os
import time

from squidwork.driver.default_chrome_driver import DefaultChromeDriver
from squidwork.driver.driver import Driver
from squidwork.actions.actions import Actions
from squidwork.logger.logger_factory import LoggerFactory

class Agent:
    def __init__(self, log_output="stdout"):
        self.cache_dir = os.path.join(os.path.expanduser("~/.cache"),  "squidwork")
        os.makedirs(self.cache_dir, exist_ok=True)
        self.logger = LoggerFactory(log_output=log_output)()
        self.logger.info(f"Logging to {self.cache_dir}")
        self.actions = self.init_actions()
        # TODO: read from batch file or single string target #2
        # TODO: fix this load from ~/.cache/squidwork/data #1

    def __call__(self, startup_browser=True):
      if startup_browser:    
        self.actions.open_browser()
      time.sleep(0.1)
        
    def init_actions(self) -> Actions:
        user_email_creds = dict()
        user_email_creds["user_email"] = os.getenv("USER_EMAIL", None)
        user_email_creds["user_email_password"] = os.getenv("USER_EMAIL_PASSWORD", None)
        return Actions(driver=self.init_driver(), logger=self.logger, cache_dir=self.cache_dir, user_email_creds=user_email_creds)
    
    def init_driver(self) -> Driver:
        driver_flags = dict()
        headless = True if os.getenv("HEADLESS", "0") == "1" else False
        driver_flags["headless"] = headless
        incognito = True if os.getenv("INCOGNITO", "0") == "1" else False
        driver_flags["incognito"] = incognito
        return DefaultChromeDriver(cache_dir=self.cache_dir, driver_flags=driver_flags).get_browser()
        

