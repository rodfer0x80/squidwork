from squidwork.bot import Bot

import os
import sys
import time

# TODO: add cicd with github actions for testing and download chrome to cache
# TODO: virtualise docker/kvm and run with windows kernel
# TODO: add frontend proxy running on client browser to hide selenium (LATE DEV) - proxy through tor for now (EARLY DEV)
# TODO: add short docs for the project

class mainBot(Bot):
    def __call__(self):
        super().__call__()
        self.actions.getURL("https://www.bing.com/search?q=Bing+AI&showconv=1&FORM=hpcodx")
        self.actions.click(by_value=("id", "bnp_btn_reject"), slow=0.5)

        # TODO: add actions support for enabling shadow root if element is not found
        # def expand_element(element):
        #     return driver.execute_script("return arguments[0].shadowRoot", element)

        # song = song_result.find_element(By.TAG_NAME, "music-button")
        # song_root = expand_element(song)
        # buttons = song_root.find_elements(By.TAG_NAME, "button")
        # buttons[1].click()

        self.actions.click(by_value=("xpath", "//cib-text-input[@product='bing']"), slow=1.5)
        #self.actions.sendKeys(by_value=("id", "searchbox"), keys="What is the best search engine?", send=True)
        time.sleep(3)
        #self.actions.sendEmail(to=["squidwork1@rodfer.online"], subject="https://gleam.io/NmBGZ/win-a-3d-printer-ender3-v2", content="https://wn.nr/DfBKjzg" )

def main():
    os.environ["HEADLESS"] = "0"
    os.environ["INCOGNITO"] = "1"
    mainBot()()
    return 0


if __name__ == '__main__':
    sys.exit(main())
