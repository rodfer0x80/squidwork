from squidwork.agent import Agent 

import os
import sys
import time

# TODO: add cicd with github actions for testing and download chrome to cache
# TODO: virtualise docker/kvm and run with windows kernel
# TODO: add frontend proxy running on client browser to hide selenium (LATE DEV) - proxy through tor for now (EARLY DEV)
# TODO: add short docs for the project

class mainAgent(Agent):
    def __call__(self):
        super().__call__()
        self.openGoogle()

    def openGoogle(self):
        search_text = input("Search: ")
        self.actions.get_url("https://google.com")
        self.actions.scroll_by(200)
        self.actions.click(("id", "L2AGLb"))
        self.actions.type(("id", "APjFqb"), search_text, send=True)
        time.sleep(10)


def main():
    os.environ["HEADLESS"] = "0"
    mainAgent()()
    return 0


if __name__ == '__main__':
    sys.exit(main())
