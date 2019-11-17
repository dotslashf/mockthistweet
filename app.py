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

fileMeme = {"output": "img/meme_new_format.png", "input": "img/meme_new.png"}
errorCode = {"private_account": 179, "blocked_account": 136, "duplicate_tweet": 187}
triggeringWords = ["please", "pliisi", "please😂", "please👏"]
dontmockme_text = ["Gaboleh nge mock creator, jangan ngelawak deh. Unique ID: ",
                   "Ya lu mau nyoba buat gue ngemock diri gue sendiri? Lucu banget. Unique ID: "]
followDulu_text = "Udah pake bot gratis apa susahnya follow dulu sih. "

FILE_LAST_ID = os.getenv("FILE_LAST_ID")
my_user_id = 1012117785512558592
my_bot_id = 1157825461277167616


def showWhatTweeted(tweet_text):  # logger
    print("------------------------------------------------",
          "\n|",
          "\n| tweeted: ", tweet_text,
          "\n| ",
          "\n------------------------------------------------")
    time.sleep(2)


def dontMockYouselfAndMe(api, tweet_text, tweet):
    '''
    Dont let the follower mock you and the bot

    Parameters:
    -----------
    @api: api object,
    @tweet_text: str,
    @tweet: Status object
    '''

    api.update_status(status=tweet_text+str(random.randint(0, 1000)),
                      in_reply_to_status_id=tweet.id,
                      auto_populate_reply_metadata=True)
    showWhatTweeted(tweet_text)


def followDuluDong(api, tweet_text, tweet):
    """
    Update status with text = followDulu_text
    if mentioning user is not a follower

    Parameters:
    -----------
    @api: api object,
    @tweet_text: str,
    @tweet: Status object
    """

    api.update_status(status=tweet_text,
                      in_reply_to_status_id=tweet.id,
                      auto_populate_reply_metadata=True)
    showWhatTweeted(tweet_text)


def checkFollowedOrNot(api, source_id, target_id):
    '''
    Show status between bot and the mentioner

    Parameters:
    -----------
    @api: api object,
    @source_id: int,
    @target_id: int
    '''

    fs = api.show_friendship(source_id=source_id, target_id=target_id)
    return fs


def mockInPliisi(api, tweet):
    '''
    Mock user with format i

    Parameters:
    -----------
    @api: api object,
    @tweet: Status object
    '''

    tweet_target = api.get_status(
        tweet.in_reply_to_status_id, tweet_mode="extended")
    k = Kalimat(tweet_target.full_text)
    textTrinsfirmid = k.trinsfirm()
    api.update_status(status=textTrinsfirmid,
                      in_reply_to_status_id=tweet.id, auto_populate_reply_metadata=True)
    showWhatTweeted(textTrinsfirmid)
    time.sleep(3)


def mockInPlease(api, tweet):
    '''
    Mock user with format spongebob meme

    Parameters:
    -----------
    @api: api object,
    @tweet: Status object
    '''

    tweet_target = api.get_status(
        tweet.in_reply_to_status_id, tweet_mode="extended")
    k = Kalimat(tweet_target.full_text)
    textTransformed = k.transform()
    drawText(textTransformed, fileMeme["input"])
    time.sleep(5)
    api.update_with_media(fileMeme["output"], status=textTransformed,
                          in_reply_to_status_id=tweet.id, auto_populate_reply_metadata=True)
    showWhatTweeted(textTransformed)


def mockInEmoji(api, tweet, emoji_type):
    '''
    Mock user with emoji format

    Parameters:
    -----------
    @api: api object,
    @tweet: Status object
    @emoji_type: str
    '''

    if emoji_type == "laugh":
        tweet_target = api.get_status(
            tweet.in_reply_to_status_id, tweet_mode="extended")
        k = Kalimat(tweet_target.full_text)
        textTransformoji = k.transformoji(emoji_type)
        api.update_status(status=textTransformoji,
                          in_reply_to_status_id=tweet.id,
                          auto_populate_reply_metadata=True)
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


def getMentionTweet(keywords, since_id, error_code):
    '''
    Get mention timeline from since_id
    to the latest_id

    Parameters:
    -----------
    @keywords: array,
    @since_id: int
    @error_code: dict
    '''

    api = tweepy.API(auth)
    new_since_id = since_id

    for tweet in tweepy.Cursor(api.mentions_timeline, since_id=since_id, tweet_mode="extended").items():
        new_since_id = max(tweet.id, new_since_id)
        print("------------------------------------------------",
              "\n| tweet id: ", tweet.id,
              "\n| username: ", tweet.user.screen_name,
              "\n| tweet: ", tweet.full_text,
              "\n------------------------------------------------\n")

        words = tweet.full_text.lower().split()

        try:
            for tw in keywords:

                if tw == "pliisi" in words:

                    # check is follower or not
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
                            mockInPliisi(api, tweet)
                    else:
                        followDuluDong(api, followDulu_text, tweet)

                elif tw == "please" in words:

                    # check is follower or not
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
                            mockInPlease(api, tweet)
                    else:
                        followDuluDong(api, followDulu_text, tweet)

                elif tw == "please😂" in words:

                    # check is follower or not
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

                elif tw == "please👏" in words:

                    # check is follower or not
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

        # throw an exception if there is err
        except tweepy.TweepError as e:
            error = e.api_code

            if error == error_code['private_account']:
                tweet_err = "Inikan private account, mana bisa gue ngeliat tweetnya"
                api.update_status(status=tweet_err,
                                  in_reply_to_status_id=tweet.id,
                                  auto_populate_reply_metadata=True)
                showWhatTweeted(tweet_err)
            elif error == error_code['blocked_account']:
                tweet_err = "Yah yang di mention ngeblock botnya"
                api.update_status(status=tweet_err,
                                  in_reply_to_status_id=tweet.id,
                                  auto_populate_reply_metadata=True)
                showWhatTweeted(tweet_err)
            elif error == error_code['duplicate_tweet']:
                tweet_err = "Duplicated"
                showWhatTweeted(tweet_err)
            else:
                print(error)
                tweet_err = "error code: "+str(error)
                api.update_status(status=tweet_err,
                                  in_reply_to_status_id=tweet.id,
                                  auto_populate_reply_metadata=True)
                showWhatTweeted(tweet_err)
                
            continue

    return new_since_id


while True:
    last_id = loadData(FILE_LAST_ID)
    last_id = int(last_id[-1])
    since_id = getMentionTweet(triggeringWords, last_id, errorCode)

    print("------------------------------------------------",
          "\n| newest tweet: ", since_id,
          "\n| oldest tweet: ", last_id,
          "\n------------------------------------------------\n")

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
