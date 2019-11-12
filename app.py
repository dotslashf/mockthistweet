import tweepy
import time
import os
from kalimat import Kalimat
from generator import drawText
from auth import authentication
from load import loadData, writeData

auth = authentication()

fileMeme = 'img/meme_final.png'
triggeringWords = ['please', 'mock', 'pls']

FILE_LAST_ID = os.getenv("FILE_LAST_ID")
last_id = loadData(FILE_LAST_ID)
last_id = int(last_id[-1])


def getMentionTweet(keywords, since_id):
    api = tweepy.API(auth)
    new_since_id = since_id

    for tweet in tweepy.Cursor(api.mentions_timeline, since_id=since_id).items():
        new_since_id = max(tweet.id, new_since_id)

        if any(keyword in tweet.text.lower() for keyword in keywords):
            tweet_target = api.get_status(tweet.in_reply_to_status_id)
            k = Kalimat(tweet_target.text)
            textNormal = k.getSentence()
            textTransformed = k.transform()
            drawText(textNormal, textTransformed, "img/meme_squared.png")
            time.sleep(5)
            api.update_with_media(
                fileMeme,
                status=textTransformed,
                in_reply_to_status_id=tweet.id,
                auto_populate_reply_metadata=True)

        # if tweet.in_reply_to_status_id is None:
        #     continue
        # if any(keyword in tweet.text.lower() for keyword in keywords):
        #     tweet_target = api.get_status(tweet.in_reply_to_status_id)
        #     k = Kalimat(tweet_target.text)
        #     textNormal = k.getSentence()
        #     textTransformed = k.transform()
        #     drawText(textNormal, "top", "img/meme_squared.png")
        #     drawText(textTransformed, "bottom", "img/meme_squared.png")
        #     print(tweet.id)
        #     time.sleep(2)
        #     # api.update_with_media(
        #     #     fileMeme,
        #     #     status=textTransformed,
        #     #     in_reply_to_status_id=tweet.id,
        #     #     auto_populate_reply_metadata=True)
    return new_since_id


getMentionTweet(triggeringWords, last_id)
