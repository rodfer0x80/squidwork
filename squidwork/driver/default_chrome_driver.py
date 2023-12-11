from selenium import webdriver
from .driver import Driver
import os

class DefaultChromeDriver(Driver):
    def __init__(self, cache_dir, driver_flags):
        headless = driver_flags["headless"]
        incognito = driver_flags["incognito"]
        super().__init__(headless=headless)
        self.cache_dir = cache_dir
        self.browser_data_dir = os.path.join(self.cache_dir, "data")
        self.browser = self.init()

    def init(self):
        self.options = webdriver.ChromeOptions()
        self.enableSystemOptions()
        self.enableStealthOptions()
        self.enableAutomationOptions()
        driver = webdriver.Chrome(
            options=self.options
        )
        driver.maximize_window()
        return driver

    def enableAutomationOptions(self):
        self.options.add_experimental_option(
            "excludeSwitches", ["enable-automation", "enable-logging"]
        )
        self.options.add_argument("--disable-dev-shm-usage") # dont touch this breaks user perms
        self.options.add_argument('--disable-blink-features=AutomationControlled')
        self.options.add_experimental_option('useAutomationExtension', False)
        self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.options.add_argument("--disable-notifications")
        self.options.add_argument("--disable-logging")
        self.options.add_argument("--silent")
        self.options.add_argument("disable-infobars")
        self.options.add_argument("--disable-crash-reporter")
        self.options.add_argument('--ignore-ssl-errors=yes')
        self.options.add_argument('--ignore-certificate-errors')
        self.options.add_argument(f"user-data-dir={self.browser_data_dir}") # cookies and browser data dir
        #self.option.add_experimental_option("detach", True) #prevent window from closing

    def enableStealthOptions(self, country_id="en-GB", incognito=False):
        # TODO: fix this with a better UA 
        #self.options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) "
        #                          "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36")
        self.options.add_argument(f"--{country_id}")
        self.options.add_argument("--window-size=1920,1080")
        if incognito:
            self.options.add_argument("--incognito")
        self.options.add_argument("--disable-gpu")
        # self.options.add_argument('--start-maximized')
        # self.options.add_argument('--start-fullscreen')
        # self.options.add_argument("--disable-extensions")


