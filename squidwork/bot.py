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
        self.headless = True if os.getenv("HEADLESS", "0") == "1" else False
        if logger == "logfile":
            self.logger = LoggerToLogfile(self.cache_dir)
        elif logger == "stdout":
            self.logger = LoggerToStdout()
        # TODO: read from batch file or single string target #2
        self.browser = DefaultChromeDriver(cache_dir=self.cache_dir, headless=self.headless).getBrowser()
        self.actions = Actions(self.browser, self.logger)
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
        threading.Thread(target=self.actions.getURL("http://localhost:1337")).start()
        self.logger.info(f"Successfully opened browser")

