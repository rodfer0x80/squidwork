from selenium.common import WebDriverException

import requests
from requests.exceptions import RequestException

import threading
from typing import Union, List, Dict

from squidwork.actions.protocols.smtpc import GmailController
from squidwork.actions.browser.browser import Browser

class Actions:
    BROWSER_INIT_URL = "http://127.0.0.1:80/"
    def __init__(self, driver, logger, cache_dir, user_email_creds:Dict[str,str]=None):
      self.cache_dir = cache_dir
        
      self.driver = driver
      self.logger = logger
      self.browser = Browser(self.driver, self.logger, self.cache_dir)
        
      self.user_email = user_email_creds["user_email"] 
      self.user_email_password = user_email_creds["user_email_password"] 

    def open_browser(self):
        threading.Thread(target=self.browser.get(self.BROWSER_INIT_URL)).start()
        self.logger.info("Successfully opened browser")
    
    def close_browser(self):
      self.browser.close()
      self.logger.info("Successfully closed browser")
    
    def request(self, url:str, method:str="GET", **kwargs) -> requests.Response:
      try:
        response = None
        if method.upper() == "GET":
          response = requests.get(url, **kwargs)
        elif method.upper() == "POST":
          response = requests.post(url, **kwargs)
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

