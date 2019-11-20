import sys
import time
import os
from dotenv import load_dotenv
from bot import Twitter
from load import loadData, writeData
from db_mongo import Database

load_dotenv()

CONSUMER_KEY = os.getenv("CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")
FILE_LAST_ID = os.getenv("FILE_LAST_ID")


def main(ck, cs, at, ats):
    bot = Twitter(ck, cs, at, ats)
    db = Database('twitter', 'tweet')

    while True:
        l = db.find_last_object()
        last_id = l['last_tweet_id']

        since_id = bot.get_mention_tweet(last_id)

        follower = bot.api.get_user(user_id=1157825461277167616)

        print("\n"+u"\u250C"+"------------------------------------------------",
              "\n| newest tweet: ", since_id,
              "\n| oldest tweet: ", last_id,
              "\n| current followers: ", follower.followers_count,
              "\n"+u"\u2514"+"------------------------------------------------")

        if (last_id != since_id):
            db.insert_object(since_id)
        else:
            print('no new mention')

        for sec in range(180, 0, -1):
            sys.stdout.write("\r")
            sys.stdout.write("{:2d} second to check mention.\r".format(sec))
            sys.stdout.flush()
            time.sleep(1)


if __name__ == "__main__":
    main(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    # bot = Twitter(CONSUMER_KEY, CONSUMER_SECRET,
    #               ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    # api_bot = bot.api
    # api_bot.update_status(status="test error code 400")
