class Driver:
    def __init__(self, headless):
        self.options = None
        self.service = None
        self.headless = headless

    def close(self):
        if self.browser:
            self.browser.close()
            self.browser.quit()
        
    def init(self):
        raise("Not implemented")

    def getBrowser(self):
        return self.browser
    
    def enableInsecureOptions(self):
        self.options.add_argument('--single-process')
        self.options.add_argument("--disable-popup-blocking")
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--disable-web-security")
        self.options.add_argument("--allow-running-insecure-content")

    def enableSystemOptions(self):
        self.options.add_argument("--disable-dev-shm-usage")
        if self.headless:
            self.options.add_argument("--headless")





