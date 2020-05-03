import tweepy
from db_mongo import Database
import os

db_name = os.environ.get("DB_NAME")

db = Database()
db.connect_db(db_name)
db.select_col('environment')

consumer_key = db.find_object('consumer_key')
consumer_secret = db.find_object('consumer_secret')

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
print('Please visit: ' + auth.get_authorization_url())

oauth_token = auth.request_token['oauth_token']
oauth_token_secret = auth.request_token['oauth_token_secret']

auth.request_token['oauth_token'] = oauth_token
auth.request_token['oauth_token_secret'] = oauth_token_secret
verifier = input('Verifier code: ')

try:
    a = auth.get_access_token(verifier)
    db.find_and_modify('access_token', a[0])
    db.find_and_modify('access_token_secret', a[1])
except tweepy.TweepError as e:
    print(e)
