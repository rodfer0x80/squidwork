import threading, os, time
from pathlib import Path
import requests

from squidwork.driver.default_chrome_driver import DefaultChromeDriver
from squidwork.actions.actions import Actions
from squidwork.logger.logger_to_logfile import LoggerToLogfile
from squidwork.logger.logger_to_stdout import LoggerToStdout

class Bot:
    def __init__(self, logger="stdout"):
        self.cache_dir = os.path.join(os.path.expanduser("~/.cache"),  "squidwork")
        os.makedirs(self.cache_dir, exist_ok=True)
        if logger == "logfile":
            self.logger = LoggerToLogfile(self.cache_dir)
        elif logger == "stdout":
            self.logger = LoggerToStdout()

        driver_flags = dict()
        headless = True if os.getenv("HEADLESS", "0") == "1" else False
        driver_flags["headless"] = headless
        incognito = True if os.getenv("INCOGNITO", "0") == "1" else False
        driver_flags["incognito"] = incognito
        self.browser = DefaultChromeDriver(cache_dir=self.cache_dir, driver_flags=driver_flags).getBrowser()

        user_email_creds = dict()
        user_email_creds["user_email"] = os.getenv("USER_EMAIL", None)
        user_email_creds["user_email_password"] = os.getenv("USER_EMAIL_PASSWORD", None)
        self.actions = Actions(self.browser, self.logger, user_email_creds=user_email_creds)

        # TODO: read from batch file or single string target #2
        # TODO: fix this load from ~/.cache/squidwork/data #1
        self.session = requests.Session()

    def __call__(self):
        self.openBrowser()
        time.sleep(0.1)

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
        threading.Thread(target=self.actions.getURL("http://www.example.com/")).start()
        self.logger.info(f"Successfully opened browser")

