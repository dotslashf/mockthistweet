import tweepy
import os
import json
from dotenv import load_dotenv
load_dotenv()

CONSUMER_KEY = os.getenv("CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")
FILE_NAMA = os.getenv("FILE_NAMA")
FILE_KALIMAT = os.getenv("FILE_KALIMAT")


def authentication():
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    return auth


auth = authentication()
api = tweepy.API(auth)

t1 = api.get_status(1194963923922866176, trim_user=True)
t2 = api.get_status(1194983890366058497, trim_user=True)
t1 = json.loads(t1.__dict__)
print(t1)
print('-------------------------------')
print(t2)

# for tweet in tweepy.Cursor(api.mentions_timeline, since_id=1194930186497581057, tweet_mode="extended").items():
#     print(tweet.full_text)
