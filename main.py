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
        self.actions.sendEmail(to=["rodrigolf080@gmail.com"], subject="Test", content="squidwork rules")
        #self.openGoogle()

    def openGoogle(self):
        self.actions.getURL("https://google.com")
        self.actions.scrollByY(200)
        by_value = ("id", "L2AGLb")
        self.actions.click(by_value)
        time.sleep(20)


def main():
    os.environ["HEADLESS"] = "0"
    mainBot()()
    return 0


if __name__ == '__main__':
    sys.exit(main())