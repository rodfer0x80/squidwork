from squidwork.bot import Bot

import sys
import time

# TODO: add cicd with github actions for testing and download chrome to cache
# TODO: virtualise docker/kvm and run with windows kernel
# TODO: add frontend proxy running on client browser to hide selenium (LATE DEV) - proxy through tor for now (EARLY DEV)
# TODO: add short docs for the project

class mainBot(Bot):
    def __call__(self):
        super().__call__()
        self.run()

    def run(self):
        self.actions.scrollByY(200)
        self.actions.click("id", "L2AGLb")
        time.sleep(3)


def main():
    mainBot()()
    return 0


if __name__ == '__main__':
    sys.exit(main())