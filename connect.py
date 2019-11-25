import tweepy
from db_mongo import Database

db = Database()
db.connect_db('twitter')
db.select_col('environment')

consumer_key = db.find_object('CONSUMER_KEY')
consumer_secret = db.find_object('CONSUMER_SECRET')

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
print('Please visit: ' + auth.get_authorization_url())

oauth_token = auth.request_token['oauth_token']
oauth_token_secret = auth.request_token['oauth_token_secret']

auth.request_token['oauth_token'] = oauth_token
auth.request_token['oauth_token_secret'] = oauth_token_secret
verifier = input('Verifier code: ')

try:
    a = auth.get_access_token(verifier)
    db.find_and_modify('ACCESS_TOKEN', a[0])
    db.find_and_modify('ACCESS_TOKEN_SECRET', a[1])
except tweepy.TweepError as e:
    print(e)
