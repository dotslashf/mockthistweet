import tweepy
import os
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


# text = ''
# for i in range(10):
#     text += '-'
#     if i == 9:
#         print(text)

# auth = authentication()
# api = tweepy.API(auth)
# tweet = api.get_status(1195779901380390913)
# mention_tl = api.mentions_timeline()
# for mention in mention_tl:
#     print(mention.text)

# for tweet in tweepy.Cursor(api.mentions_timeline, since_id=1194930186497581057, tweet_mode="extended").items():
#     print(tweet.full_text)
