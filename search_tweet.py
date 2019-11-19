from bot import Twitter
from load import loadData
import os
from dotenv import load_dotenv

load_dotenv()

CONSUMER_KEY = os.getenv("CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")

bot = Twitter(CONSUMER_KEY, CONSUMER_SECRET,
              ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

tweet_bug = bot.api.get_status(id=1196782210642333696, include_entities=False)
tweet = bot.api.get_status(id=1196799891961307136)

# for key, entities in tweet_bug.entities.items():
#     for value in entities:
#         print(value['screen_name'])

# print('\n')

# for tweet in tweet.entities.items():
#     for a in tweet[1]:
#         last = list(a.items())[0][-1]
# print(last)


print(tweet_bug.text)
