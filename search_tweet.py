import tweepy
from bot import Twitter
from db_mongo import Database

db = Database()
db.connect_db('twitter')
db.select_col('environment')

consumer_key = db.find_object('CONSUMER_KEY')
consumer_secret = db.find_object('CONSUMER_SECRET')
access_token = db.find_object('ACCESS_TOKEN')
access_token_secret = db.find_object('ACCESS_TOKEN_SECRET')

bot = Twitter(consumer_key, consumer_secret, access_token, access_token_secret)

list_tweet = []

for tweet in tweepy.Cursor(bot.api.mentions_timeline,
                           since_id=1199008704076505092,
                           max_id=1199009095925161992,
                           tweet_mode="extended").items():
    list_tweet.append(tweet.full_text)

for t in reversed(list_tweet):
    print(t)
