from squidwork.agent import Agent

import os
import sys
import time

# TODO: add cicd with github actions for testing and download chrome to cache
# TODO: virtualise docker/kvm and run with windows kernel
# TODO: add frontend proxy running on client browser to hide selenium (LATE DEV) - proxy through tor for now (EARLY DEV)
# TODO: add short docs for the project

class SearchAgent(Agent):
    def __call__(self):
        super().__call__()
        self.searchGoogle()

    def searchGoogle(self):
        search_text = "squidwork rules"
        self.actions.get_url("https://google.com")
        self.actions.scroll(n=1)
        self.actions.click(by_value=("name", "q"))
        self.actions.type(by_value=("name", "q"), keys=search_text, send=True)
        self.actions.scroll(n=3)
        time.sleep(4.0)


def main():
    os.environ["HEADLESS"] = "0"
    os.environ['INCOGNITO'] = "1"
    SearchAgent()()
    return 0


if __name__ == '__main__':
    sys.exit(main())