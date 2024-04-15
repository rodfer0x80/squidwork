import os
import pickle

class Cookies:
  def __init__(self, cache_dir, logger, browser):
    self.cache_dir = os.path.join(cache_dir, "cookies")
    os.makedirs(self.cache_dir, exist_ok=True)
    self.logger = logger
    self.browser = browser

  def get_cookies(self):
    return self.browser.get_cookies()

  def import_cookies(self, filename):
    try:
      with open(os.path.join(self.cache_dir, filename+".pkl"), 'rb') as fp:
        cookies = pickle.load(fp)
        for cookie in cookies:
          self.browser.add_cookie(cookie)
      self.logger.info(f"Imported cookies from {self.cache_dir}/{filename}.pkl")
    except Exception as e:
      self.logger.log(f"cookies.py:23 - No cookies imported. Error: {e}")
      return 1  
    return 0  

  def export_cookies(self, filename):
    try:
      with open(os.path.join(self.cache_dir, filename+".pkl"), 'wb') as fp:
        pickle.dump(self.browser.get_cookies(), fp)
      self.logger.info(f"Exported cookies to {self.cache_dir}/{filename}.pkl")
    except Exception as e:
      self.logger.log(f"cookies.py:32 - No cookies exported. Error: {e}")
      return 1
    return 0

