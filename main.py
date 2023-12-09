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
        self.openGoogle()

    def openGoogle(self):
        search_text = "test"
        self.actions.getURL("https://google.com")
        self.actions.scrollByY(200)
        self.actions.click(("id", "L2AGLb"))
        self.actions.sendKeys(("id", "APjFqb"), search_text, send=True)
        time.sleep(5)


def main():
    os.environ["HEADLESS"] = "0"
    mainBot()()
    return 0


if __name__ == '__main__':
    sys.exit(main())
