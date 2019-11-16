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
triggeringWords = ["please", "pliisi", "ple😂se", "ple👏se"]
my_user_id = 1012117785512558592
my_bot_id = 1157825461277167616
dontmockme_text = ["ye enak aja yang punya bot mau di mock, unique id: ", "ya masa gue ngemock diri gue sendiri ya nggalah, unique id: "]
followDulu_text = "Follow dulu dong kak. "

FILE_LAST_ID = os.getenv("FILE_LAST_ID")


def showWhatTweeted(tweet_text): #logger
    print("#######################################################")
    print("tweeted: ", tweet_text)
    print("#######################################################")
    time.sleep(2)

def dontMockYouselfAndMe(api, tweet_text, tweet):  # dont mock the creator
    api.update_status(status=tweet_text+str(random.randint(0, 1000)),
                      in_reply_to_status_id=tweet.id,
                      auto_populate_reply_metadata=True)
    showWhatTweeted(tweet_text)

def followDuluDong(api, tweet_text, tweet): # tweet when mentioned user is not follower
    api.update_status(status=tweet_text,
                    in_reply_to_status_id=tweet.id,
                    auto_populate_reply_metadata=True)
    showWhatTweeted(tweet_text)

def checkFollowedOrNot(api, source_id, target_id):
    fs = api.show_friendship(source_id=source_id, target_id=target_id)
    return fs

def mockInPliisi(api, tweet):
    tweet_target = api.get_status(tweet.in_reply_to_status_id, tweet_mode="extended")
    k = Kalimat(tweet_target.full_text)
    textTrinsfirmid = k.trinsfirm()
    api.update_status(status=textTrinsfirmid, in_reply_to_status_id=tweet.id, auto_populate_reply_metadata=True)
    showWhatTweeted(textTrinsfirmid)
    time.sleep(3)

def mockInPlease(api, tweet):
    tweet_target = api.get_status(tweet.in_reply_to_status_id, tweet_mode="extended")
    k = Kalimat(tweet_target.full_text)
    textTransformed = k.transform()
    drawText(textTransformed, fileMemeOriginal)
    time.sleep(5)
    api.update_with_media(fileMeme, status=textTransformed, in_reply_to_status_id=tweet.id, auto_populate_reply_metadata=True)
    showWhatTweeted(textTransformed)

def mockInEmoji(api, tweet, emoji_type):
    if emoji_type == "laugh":
        tweet_target = api.get_status(tweet.in_reply_to_status_id, tweet_mode="extended")
        k = Kalimat(tweet_target.full_text)
        textTransformoji = k.transformoji(emoji_type)
        api.update_status(status=textTransformoji, in_reply_to_status_id=tweet.id, auto_populate_reply_metadata=True)
        showWhatTweeted(textTransformoji)
        time.sleep(3)

    elif emoji_type == "clap":
        tweet_target = api.get_status(
            tweet.in_reply_to_status_id, tweet_mode="extended")
        k = Kalimat(tweet_target.full_text)
        textTransformoji = k.transformoji(emoji_type)
        api.update_status(status=textTransformoji,
                          in_reply_to_status_id=tweet.id, auto_populate_reply_metadata=True)
        showWhatTweeted(textTransformoji)
        time.sleep(3)

def getMentionTweet(keywords, since_id):
    api = tweepy.API(auth)
    new_since_id = since_id

    for tweet in tweepy.Cursor(api.mentions_timeline, since_id=since_id, tweet_mode="extended").items():
        new_since_id = max(tweet.id, new_since_id)
        print("current tweet id: ", tweet.id, "tweet: ", tweet.full_text)

        words = tweet.full_text.lower().split()

        try:
            for tw in triggeringWords:
                if tw == "pliisi" in words:

                    #check is follower or not
                    follower_status = checkFollowedOrNot(api, my_bot_id, tweet.user.id)

                    if (follower_status[0].followed_by):
                        if my_user_id == tweet.in_reply_to_user_id:
                            dontMockYouselfAndMe(
                                api, dontmockme_text[0], tweet)
                        elif my_bot_id == tweet.in_reply_to_user_id:
                            dontMockYouselfAndMe(
                                api, dontmockme_text[1], tweet)
                        else:
                            mockInPliisi(api, tweet)
                    else:
                        followDuluDong(api, followDulu_text, tweet)

                elif tw == "please" in words:

                    #check is follower or not
                    follower_status = checkFollowedOrNot(
                        api, my_bot_id, tweet.user.id)

                    if (follower_status[0].followed_by):
                        if my_user_id == tweet.in_reply_to_user_id:
                            dontMockYouselfAndMe(api, dontmockme_text[0], tweet)
                        elif my_bot_id == tweet.in_reply_to_user_id:
                            dontMockYouselfAndMe(api, dontmockme_text[1], tweet)
                        else:
                            mockInPlease(api, tweet)
                    else:
                        followDuluDong(api, followDulu_text, tweet)

                elif tw == "ple😂se" in words:
                    #check is follower or not
                    follower_status = checkFollowedOrNot(
                        api, my_bot_id, tweet.user.id)

                    if (follower_status[0].followed_by):
                        if my_user_id == tweet.in_reply_to_user_id:
                            dontMockYouselfAndMe(
                                api, dontmockme_text[0], tweet)
                        elif my_bot_id == tweet.in_reply_to_user_id:
                            dontMockYouselfAndMe(
                                api, dontmockme_text[1], tweet)
                        else:
                            mockInEmoji(api, tweet, "laugh")
                    else:
                        followDuluDong(api, followDulu_text, tweet)

                elif tw == "ple👏se" in words:
                    #check is follower or not
                    follower_status = checkFollowedOrNot(
                        api, my_bot_id, tweet.user.id)

                    if (follower_status[0].followed_by):
                        if my_user_id == tweet.in_reply_to_user_id:
                            dontMockYouselfAndMe(
                                api, dontmockme_text[0], tweet)
                        elif my_bot_id == tweet.in_reply_to_user_id:
                            dontMockYouselfAndMe(
                                api, dontmockme_text[1], tweet)
                        else:
                            mockInEmoji(api, tweet, "clap")
                    else:
                        followDuluDong(api, followDulu_text, tweet)


        except tweepy.TweepError as e:
            error_code = e.api_code
            errorPrivateAcc = 179
            errorBlocked = 136
            if errorPrivateAcc == error_code:
                tweet_err = "akunnya ke kunci, gimana caranya gue mock hAdEh"
                api.update_status(status=tweet_err,
                                    in_reply_to_status_id=tweet.id,
                                    auto_populate_reply_metadata=True)
                showWhatTweeted(tweet_err)
            elif errorBlocked == error_code:
                tweet_err = "sayangnya gue diblock sama user yang mau lo mock, cari korban yang lain"
                api.update_status(status=tweet_err,
                                  in_reply_to_status_id=tweet.id,
                                  auto_populate_reply_metadata=True)
                showWhatTweeted(tweet_err)
            else:
                print(error_code)
                tweet_err = "error code: "+str(error_code)
                api.update_status(status=tweet_err,
                                  in_reply_to_status_id=tweet.id,
                                  auto_populate_reply_metadata=True)
                showWhatTweeted(tweet_err)
            continue
            
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
