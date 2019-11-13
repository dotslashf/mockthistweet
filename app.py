import sys
import tweepy
import time
import os
from kalimat import Kalimat
from generator import drawText
from auth import authentication
from load import loadData, writeData

auth = authentication()

fileMeme = 'img/meme_new_format.png'
fileMemeOriginal = 'img/meme_new.png'
triggeringWords = ["please", "pliisi"]

FILE_LAST_ID = os.getenv("FILE_LAST_ID")


def getMentionTweet(keywords, since_id):
    api = tweepy.API(auth)
    new_since_id = since_id

    for tweet in tweepy.Cursor(api.mentions_timeline, since_id=since_id).items():
        new_since_id = max(tweet.id, new_since_id)

        words = tweet.text.split()

        for tw in triggeringWords:
            if tw == "pliisi" in words:
                tweet_target = api.get_status(tweet.in_reply_to_status_id)
                k = Kalimat(tweet_target.text)
                textTrinsfirmid = k.trinsfirm()
                api.update_status(status=textTrinsfirmid, in_reply_to_status_id=tweet.id,
                                  auto_populate_reply_metadata=True)
                print("tweeted: ", textTrinsfirmid)
                time.sleep(15)
            elif tw == "please" in words:
                tweet_target = api.get_status(tweet.in_reply_to_status_id)
                k = Kalimat(tweet_target.text)
                textTransformed = k.transform()
                drawText(textTransformed, fileMemeOriginal)
                time.sleep(15)
                api.update_with_media(
                    fileMeme,
                    status=textTransformed,
                    in_reply_to_status_id=tweet.id,
                    auto_populate_reply_metadata=True)
                print("tweeted: ", textTransformed)

    return new_since_id


while True:
    last_id = loadData(FILE_LAST_ID)
    last_id = int(last_id[-1])
    since_id = getMentionTweet(triggeringWords, last_id)
    print("newest tweet: ", since_id, "oldest tweet: ", last_id)
    if (last_id != since_id):
        writeData(FILE_LAST_ID, str(since_id))
    else:
        print('no new mention')
    for sec in range(300, 0, -1):
        sys.stdout.write("\r")
        sys.stdout.write("{:2d} second to check mention.\r".format(sec))
        sys.stdout.flush()
        time.sleep(1)

# Testing purpose
# last_id = loadData(FILE_LAST_ID)
# last_id = int(last_id[-1])
# print(getMentionTweet(triggeringWords, 1194499648083226626))
# api = tweepy.API(auth)

# tweet_target = api.get_status(1194254123463393282)

# for property, value in vars(tweet_target).items():
#     print (property, ": ", value)
