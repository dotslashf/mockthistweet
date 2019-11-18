import sys
import time
import os
from dotenv import load_dotenv
from bot import Twitter
from load import loadData, writeData

load_dotenv()

CONSUMER_KEY = os.getenv("CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")
FILE_LAST_ID = os.getenv("FILE_LAST_ID")


def main(ck, cs, at, ats):
    bot = Twitter(ck, cs, at, ats)

    while True:
        last_id = loadData(FILE_LAST_ID)
        last_id = int(last_id[-1])
        since_id = bot.get_mention_tweet(last_id)

        print("------------------------------------------------",
              "\n| newest tweet: ", since_id,
              "\n| oldest tweet: ", last_id,
              "\n------------------------------------------------\n")

        if (last_id != since_id):
            writeData(FILE_LAST_ID, str(since_id))
        else:
            print('no new mention')

        for sec in range(180, 0, -1):
            sys.stdout.write("\r")
            sys.stdout.write("{:2d} second to check mention.\r".format(sec))
            sys.stdout.flush()
            time.sleep(1)


if __name__ == "__main__":
    main(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
