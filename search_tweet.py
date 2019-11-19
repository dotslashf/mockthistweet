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

tweet = bot.api.get_status(id=1196628742044446720)

print(tweet.text)
