from squidwork.agent import Agent 

import os
import sys
import time

# TODO: add cicd with github actions for testing and download chrome to cache
# TODO: virtualise docker/kvm and run with windows kernel
# TODO: add frontend proxy running on client browser to hide selenium (LATE DEV) - proxy through tor for now (EARLY DEV)
# TODO: add short docs for the project

class mainAgent(Agent):
  def __init__(self, init_url="https://setcookie.net", log_output="stdout"):
    super().__init__(init_url, log_output)

  def __call__(self):
    super().__call__()
    self.test_cookies()

  def test_cookies(self):
    self.actions.get_url("https://setcookie.net")
    #self.actions.scroll_by(200)
    time.sleep(2)
    self.actions.click(("name", "name"))
    self.actions.type(("name", "name"), "cookie_tester_name", send=True)
    self.actions.click(("name", "value"))
    self.actions.type(("name", "value"), "cookie_tester_value", send=True)
    self.actions.click(("xpath", '//input[@type="submit"]'))
    self.save_state()
    time.sleep(2)


def main():
  os.environ["HEADLESS"] = "0"
  mainAgent()()
  return 0


if __name__ == '__main__':
  sys.exit(main())
