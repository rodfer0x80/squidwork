import sys
from squidwork.bot import Bot

# connect to meta api
# search instagram posts
# read instagram posts to terminal
# write instagram posts
# filter and comment on instagram posts
# repeat but with facebook


def main():
  bot = Bot()
  bot.actions.sendEmail(to=["squidwork1@rodfer.online", "team.arkint.ai@gmail.com"], subject="Test", content="squidwork rules", n=10)
  return 0


if __name__ == '__main__':
    sys.exit(main())
