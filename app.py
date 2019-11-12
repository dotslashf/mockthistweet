import tweepy
import time
import os
from kalimat import Kalimat
from generator import drawText
from auth import authentication

auth = authentication()

fileMeme = 'img/meme_final.png'


def getMentionTweet(since_id):
    api = tweepy.API(auth)
    new_since_id = since_id

    for tweet in tweepy.Cursor(api.mentions_timeline, since_id=since_id).items():
        new_since_id = max(tweet.id, new_since_id)
        print(tweet.in_reply_to_status_id)

        if tweet.in_reply_to_status_id is not None:
            if 'please' in tweet.text.lower():
                tweet_target = api.get_status(tweet.in_reply_to_status_id)
                k = Kalimat(tweet_target.text)
                textNormal = k.getSentence()
                textTransformed = k.transform()
                drawText(textNormal, "top")
                drawText(textTransformed, "bottom")
                time.sleep(2)
                api.update_with_media(
                    fileMeme, 
                    in_reply_to_status_id=tweet.id, 
                    auto_populate_reply_metadata=True)

    return new_since_id


getMentionTweet(1185320500144164865)
