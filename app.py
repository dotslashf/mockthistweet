import sys
import tweepy
import time
import os
import random
from kalimat import Kalimat
from generator import drawText
from auth import authentication
from load import loadData, writeData

auth = authentication()

fileMeme = 'img/meme_new_format.png'
fileMemeOriginal = 'img/meme_new.png'
triggeringWords = ["please", "pliisi"]
my_user_id = 1012117785512558592
my_bot_id = 1157825461277167616
youdontmockme = "ye enak aja yang punya bot mau di mock, gak boleh kurang ajar. unique id: "
followdulu = "Follow dulu dong kak, ini aku follow kakak deh. "

FILE_LAST_ID = os.getenv("FILE_LAST_ID")


def dontMockYouselfAndMe(api, tweet, tweet_id):  # dont mock the creator
    api.update_status(status=tweet+str(random.randint(0, 1000)),
                      in_reply_to_status_id=tweet_id,
                      auto_populate_reply_metadata=True)
    print("tweeted: ", tweet)
    time.sleep(5)

def followDuluDong(api, my_tweet, tweet): # tweet when mentioned user is not follower
    api.update_status(status=my_tweet,
                    in_reply_to_status_id=tweet.id,
                    auto_populate_reply_metadata=True)
    api.create_friendship(id=tweet.user.id)  # follow the user
    print("tweeted: ", my_tweet)
    print("user: ", tweet.user.name, " followed")
    time.sleep(5)


def getMentionTweet(keywords, since_id):
    api = tweepy.API(auth)
    new_since_id = since_id

    for tweet in tweepy.Cursor(api.mentions_timeline, since_id=since_id, tweet_mode="extended").items():
        new_since_id = max(tweet.id, new_since_id)

        words = tweet.full_text.lower().split()

        try:
            for tw in triggeringWords:
                if tw == "pliisi" in words:
                    follower_status = api.show_friendship(source_id=my_bot_id,
                                                        target_id=tweet.user.id)
                    if (follower_status[0].followed_by):
                        api.create_friendship(id=tweet.user.id)  # follow the user
                        if my_user_id == tweet.in_reply_to_user_id or my_bot_id == tweet.in_reply_to_user_id:
                            dontMockYouselfAndMe(api, youdontmockme, tweet.id)
                        else:
                            tweet_target = api.get_status(tweet.in_reply_to_status_id, 
                                                          tweet_mode="extended")
                            k = Kalimat(tweet_target.full_text)
                            textTrinsfirmid = k.trinsfirm()
                            api.update_status(status=textTrinsfirmid,
                                            in_reply_to_status_id=tweet.id,
                                            auto_populate_reply_metadata=True)
                            print("tweeted: ", textTrinsfirmid)
                            time.sleep(15)
                    else:
                        followDuluDong(api, followdulu, tweet)

                elif tw == "please" in words:
                    follower_status = api.show_friendship(source_id=my_bot_id,
                                                        target_id=tweet.user.id)

                    # get status, false = tidak follow, true = follower
                    if (follower_status[0].followed_by):
                        api.create_friendship(id=tweet.user.id)  # follow the user
                        if my_user_id == tweet.in_reply_to_user_id or my_bot_id == tweet.in_reply_to_user_id:
                            dontMockYouselfAndMe(api, youdontmockme, tweet.id)
                        else:
                            tweet_target = api.get_status(tweet.in_reply_to_status_id,
                                                          tweet_mode="extended")
                            k = Kalimat(tweet_target.full_text)
                            textTransformed = k.transform()
                            drawText(textTransformed, fileMemeOriginal)
                            time.sleep(15)
                            api.update_with_media(
                                fileMeme,
                                status=textTransformed,
                                in_reply_to_status_id=tweet.id,
                                auto_populate_reply_metadata=True)
                            print("tweeted: ", textTransformed)
                    else:
                        followDuluDong(api, followdulu, tweet)

        except Exception as e:
            print(e)
            return new_since_id
            
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
    for sec in range(180, 0, -1):
        sys.stdout.write("\r")
        sys.stdout.write("{:2d} second to check mention.\r".format(sec))
        sys.stdout.flush()
        time.sleep(1)

# Testing purpose
# last_id = loadData(FILE_LAST_ID)
# last_id = int(last_id[-1])
# print(getMentionTweet(triggeringWords, 1194701185317343232))
# api = tweepy.API(auth)

# for property, value in vars(tweet_target).items():
#     print (property, ": ", value)
# my user id 1012117785512558592
