import tweepy
import os
from dotenv import load_dotenv

load_dotenv()

CONSUMER_KEY = os.getenv("CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
print('Please visit: ' + auth.get_authorization_url())

oauth_token = auth.request_token['oauth_token']
oauth_token_secret = auth.request_token['oauth_token_secret']

auth.request_token['oauth_token'] = oauth_token
auth.request_token['oauth_token_secret'] = oauth_token_secret
verifier = input('Verifier code: ')

try:
    a = auth.get_access_token(verifier)
    print(a)
except tweepy.TweepError as e:
    print(e)
