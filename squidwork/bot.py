import threading, os, time
from pathlib import Path
import requests

from squidwork.driver.default_chrome_driver import DefaultChromeDriver
from squidwork.actions.actions import Actions
from squidwork.logger.logger_to_logfile import LoggerToLogfile

class Bot:
    def __init__(self):
        self.cache_dir = Path(os.path.join((os.path.expanduser(\
            os.getenv("XDG_HOME_CACHE", "~/.cache"))),  "squidwork"))
        os.makedirs(self.cache_dir, exist_ok=True)
        self.logger = LoggerToLogfile(self.cache_dir)
        # TODO: read from batch file or single string target
        self.target = "https://google.com"
        self.headless = True if os.getenv("HEADLESS", "0") == "1" else False
        self.browser = DefaultChromeDriver(
            target=self.target, cache_dir=self.cache_dir, headless=self.headless).getBrowser()
        self.actions = Actions(self.browser, self.logger)
        # TODO: fix this
        self.session = requests.Session()


    def __call__(self):
        self.openBrowser()
        time.sleep(0.1)

    # TODO: fix this ? load from ~/.cache/data
    # TODO: we investigate
    def addCookiesToSession(self):
        try:
            # TODO: implement this
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
        threading.Thread(target=self.actions.getURL(self.target)).start()
        self.logger.info(f"Successfully opened browser")
