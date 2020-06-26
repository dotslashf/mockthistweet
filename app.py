import sys
import time
import os
from bot import Twitter
from db_mongo import Database

db_name = os.environ.get("DB_MOCKTHISTWEET")

db = Database()
db.connect_db(db_name)
db.select_col('environment')

consumer_key = db.find_object('consumer_key')
consumer_secret = db.find_object('consumer_secret')
access_token = db.find_object('access_token')
access_token_secret = db.find_object('access_token_secret')


def main(ck, cs, at, ats):
    bot = Twitter(ck, cs, at, ats)
    db = Database()
    db.connect_db(db_name)
    db.select_col('tweet')

    minute_wait = 5

    while True:
        l = db.find_last_object()
        last_id = l['tweet_last_id']

        since_id = bot.get_mention_tweet(last_id)

        me = bot.api.me()
        my_current_followers = me.followers_count
        bot.follower_counter(my_current_followers)

        t = time.localtime()
        current_time = time.strftime("%H:%M:%S %D", t)

        print("\n"+u"\u250C"+"------------------------------------------------",
              "\n| current time: ", current_time,
              "\n| newest tweet: ", since_id,
              "\n| oldest tweet: ", last_id,
              "\n| current followers: ", me.followers_count,
              "\n| total tweets: ", me.statuses_count,
              "\n"+u"\u2514"+"------------------------------------------------")

        if (last_id != since_id):
            db.insert_object({'tweet_last_id': since_id})
        else:
            print('no new mention')

        for sec in range(minute_wait * 60, 0, -1):
            sys.stdout.write("\r")
            sys.stdout.write("{:2d} second to check mention.\r".format(sec))
            sys.stdout.flush()
            time.sleep(1)


if __name__ == "__main__":
    main(consumer_key, consumer_secret, access_token, access_token_secret)
