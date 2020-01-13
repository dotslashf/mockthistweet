import tweepy
import os
import time
from datetime import datetime
from dateutil import relativedelta
from generator import drawText
from kalimat import Kalimat
from emoji_generator import Emoji
from db_mongo import Database


class Twitter:
    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret
        self.auth = self.authentication()
        self.api = tweepy.API(self.auth)
        self.error_code = {
            "private_account": [179, "Kalau mau ngemock pikir-pikir juga dong, masa private akun, mana keliatan tweetnya "],
            "blocked_account": [136, "Botnya dah diblock sama doi, ah ga seru "],
            "duplicate_tweet": [187, "Duplicated tweet"],
            "tweet_target_deleted": [144, "Tweetnya udah dihapus, kasian deh lo"],
            "tweet_target_to_long": [186, "Tweetnya kepanjangan kalau di tambahin emoji, coba format yang lain"],
            "tweet_deleted_or_not_visible": [385, "Tweet deleted or not visible"],
            "twitter_over_capacity": [130, "Twitternya lagi overcapacity, next time yah"],
            "page_does_not_exist": [34, "Pages does not exist"],
            "suspended_account": [63, "Yang mau dimock dah disuspend, twitter, mampus."]
        }
        self.triggering_words = ["please", "pliisi",
                                 "please😂", "please👏",
                                 "please🤮", "please🤢",
                                 "pleasek", "pleaseb", "pleasej",
                                 "please💩"]
        self.my_user_id = 1012117785512558592
        self.my_bot_id = 1157825461277167616
        self.tweet_text = {
            "dont_mock": ["Enak aja developernya mau di mock, jangan ngelawak deh ",
                          " adalah orang yang paling gabut, gak usah nyoba buat ngebuat botnya ngemock diri sendiri."],
            "follow_dulu": "Follow dulu, kalau gak mau ya mock manual aja yah ",
            "untag_dong": "Kalau jelasin cara kerja botnya tolong di untag yah, "
        }
        self.file_meme = {"output": ["img/meme_spongebob_output.png", "img/meme_khaleesi_output.png"],
                          "input": ["img/meme_new.png", "img/meme_khaleesi.png"]}
        self.time_interval = 30

    def authentication(self):
        self.auth = tweepy.OAuthHandler(
            self.consumer_key, self.consumer_secret)
        self.auth.set_access_token(self.access_token, self.access_token_secret)
        return self.auth

    def check_follower(self, source_id, target_id):
        fs = self.api.show_friendship(source_id=source_id, target_id=target_id)
        return fs

    def account_old(self, user_old):
        today = datetime.now()
        diff = relativedelta.relativedelta(today, user_old)
        return diff.months+(diff.years*12)

    def show_what_tweeted(self, tweet_text):  # logger
        print(u"\u250C"+"-----------------------------------------------",
              "\n|",
              "\n| tweeted: ", tweet_text,
              "\n| ",
              "\n"+u"\u2514"+"-----------------------------------------------")

    def show_status(self, tweet):
        print(u"\u250C"+"-----------------------------------------------",
              "\n| tweet id: ", tweet.id,
              "\n| username: ", tweet.user.screen_name,
              "\n| tweet: ", tweet.full_text,
              "\n"+u"\u2514"+"-----------------------------------------------")

    def tweeted_and_show(self, tweet_text, tweet, position):
        username = tweet.user.screen_name

        if position == 'back':
            tweet_text = tweet_text+username
        elif position == 'front':
            tweet_text = '@'+username+tweet_text

        try:
            self.api.update_status(status=tweet_text,
                                   in_reply_to_status_id=tweet.id,
                                   auto_populate_reply_metadata=True)
            self.show_what_tweeted(tweet_text)
        except tweepy.TweepError as e:
            print(e.api_code, e.response)
        time.sleep(self.time_interval)

    def mock_in_pliisi(self, tweet, db):
        tweet_target = self.api.get_status(tweet.in_reply_to_status_id,
                                           tweet_mode="extended")
        k = Kalimat(tweet_target.full_text)
        text_trinsfirmid = k.trinsfirm()
        drawText(text_trinsfirmid, self.file_meme["input"][1], "khaleesi")
        self.api.update_with_media(filename=self.file_meme["output"][1],
                                   status=text_trinsfirmid,
                                   in_reply_to_status_id=tweet.id,
                                   auto_populate_reply_metadata=True)
        self.show_what_tweeted(text_trinsfirmid)
        db.insert_object({'tweet_last_id': tweet.id})

    def mock_in_please(self, tweet, db):
        tweet_target = self.api.get_status(tweet.in_reply_to_status_id,
                                           tweet_mode="extended")
        k = Kalimat(tweet_target.full_text)
        text_transformed = k.transform()
        drawText(text_transformed, self.file_meme["input"][0], "spongebob")
        self.api.update_with_media(filename=self.file_meme["output"][0],
                                   status=text_transformed,
                                   in_reply_to_status_id=tweet.id,
                                   auto_populate_reply_metadata=True)
        self.show_what_tweeted(text_transformed)
        db.insert_object({'tweet_last_id': tweet.id})

    def mock_in_emoji(self, tweet, emoji_type, db):
        tweet_target = self.api.get_status(
            tweet.in_reply_to_status_id, tweet_mode="extended")
        k = Kalimat(tweet_target.full_text)

        if emoji_type == "laugh":
            text_transformoji = k.transformoji(emoji_type)
            self.api.update_status(status=text_transformoji,
                                   in_reply_to_status_id=tweet.id,
                                   auto_populate_reply_metadata=True)
            self.show_what_tweeted(text_transformoji)

        elif emoji_type == "clap":
            text_transformoji = k.transformoji(emoji_type)
            self.api.update_status(status=text_transformoji,
                                   in_reply_to_status_id=tweet.id,
                                   auto_populate_reply_metadata=True)
            self.show_what_tweeted(text_transformoji)

        elif emoji_type == "vomit":
            text_transformoji = k.transformoji(emoji_type)
            self.api.update_status(status=text_transformoji,
                                   in_reply_to_status_id=tweet.id,
                                   auto_populate_reply_metadata=True)
            self.show_what_tweeted(text_transformoji)

        elif emoji_type == "sick":
            text_transformoji = k.transformoji(emoji_type)
            self.api.update_status(status=text_transformoji,
                                   in_reply_to_status_id=tweet.id,
                                   auto_populate_reply_metadata=True)
            self.show_what_tweeted(text_transformoji)

        elif emoji_type == "poop":
            text_transformoji = k.transformoji(emoji_type)
            text_tambahan = "{} alias tai semua yg lo tweet".format(
                text_transformoji)
            self.api.update_status(status=text_tambahan,
                                   in_reply_to_status_id=tweet.id,
                                   auto_populate_reply_metadata=True)
            self.show_what_tweeted(text_tambahan)

        db.insert_object({'tweet_last_id': tweet.id})

    def mock_in_emoji_pattern(self, tweet, pattern, db):
        tweet_target = self.api.get_status(tweet.in_reply_to_status_id,
                                           tweet_mode="extended")
        k = Kalimat(tweet_target.full_text)
        words = k.sentence
        words = [i for j in words.split() for i in (j, ' ')][:-1]

        target_name = tweet_target.user.screen_name

        for word in words:
            if word in k.excludedWords:
                target_name = 'nder'

        if pattern == 'k':
            e = Emoji("kamu mending tutup akun twitter aja ")
            re = e.random()
            e.pick_emoji(re)
            text_k = e.create_pattern(pattern)
            text_k += target_name
            self.api.update_status(status=text_k,
                                   in_reply_to_status_id=tweet.id,
                                   auto_populate_reply_metadata=True)
            self.show_what_tweeted(text_k)
        elif pattern == 'b':
            e = Emoji("bacot banget lu ")
            re = e.random()
            e.pick_emoji(re)
            text_b = e.create_pattern(pattern)
            text_b += target_name
            self.api.update_status(status=text_b,
                                   in_reply_to_status_id=tweet.id,
                                   auto_populate_reply_metadata=True)
            self.show_what_tweeted(text_b)
        elif pattern == 'j':
            e = Emoji("jancok! raimu iku loh ")
            re = e.random()
            e.pick_emoji(re)
            text_j = e.create_pattern(pattern)
            text_j += target_name
            self.api.update_status(status=text_j,
                                   in_reply_to_status_id=tweet.id,
                                   auto_populate_reply_metadata=True)
            self.show_what_tweeted(text_j)

        db.insert_object({'tweet_last_id': tweet.id})

    def am_i_mentioned(self, tweet):
        for t in tweet.entities.items():
            for a in t[1]:
                last = list(a.items())[0][-1]
        return last

    def process_mention(self, list_tweet):
        db = Database()
        db.connect_db('twitter')
        db.select_col('tweet')

        for tweet in reversed(list_tweet):
            self.show_status(tweet)
            try:
                words = tweet.full_text.lower().split()
                if self.my_user_id == tweet.in_reply_to_user_id:
                    for tw in self.triggering_words:
                        if tw in words:
                            self.tweeted_and_show(
                                self.tweet_text["dont_mock"][0], tweet, 'back')
                elif self.my_bot_id == tweet.in_reply_to_user_id:
                    for tw in self.triggering_words:
                        if tw in words:
                            self.tweeted_and_show(
                                self.tweet_text["dont_mock"][1], tweet, 'front')
                else:
                    for tw in self.triggering_words:
                        if tw is "pliisi" in words:
                            self.mock_in_pliisi(tweet, db)

                        elif tw is "please" in words:
                            self.mock_in_please(tweet, db)

                        elif tw is "pleasek" in words:
                            self.mock_in_emoji_pattern(tweet, 'k', db)

                        elif tw is "pleaseb" in words:
                            self.mock_in_emoji_pattern(tweet, 'b', db)

                        elif tw is "pleasej" in words:
                            self.mock_in_emoji_pattern(tweet, 'j', db)

                        elif tw == "please😂" in words:
                            self.mock_in_emoji(tweet, "laugh", db)

                        elif tw == "please👏" in words:
                            self.mock_in_emoji(tweet, "clap", db)

                        elif tw == "please🤮" in words:
                            self.mock_in_emoji(tweet, "vomit", db)

                        elif tw == "please🤢" in words:
                            self.mock_in_emoji(tweet, "sick", db)

                        elif tw == "please💩" in words:
                            self.mock_in_emoji(tweet, "poop", db)

            except tweepy.TweepError as e:
                error = e.api_code
                error_text = e.response

                db.insert_object({'tweet_last_id': tweet.id})

                if error == self.error_code['private_account'][0]:
                    tweet_err = self.error_code['private_account'][1]
                    self.api.update_status(status=tweet_err,
                                           in_reply_to_status_id=tweet.id,
                                           auto_populate_reply_metadata=True)
                    self.show_what_tweeted(tweet_err)

                elif error == self.error_code['blocked_account'][0]:
                    tweet_err = self.error_code['blocked_account'][1]
                    self.api.update_status(status=tweet_err,
                                           in_reply_to_status_id=tweet.id,
                                           auto_populate_reply_metadata=True)
                    self.show_what_tweeted(tweet_err)

                elif error == self.error_code['tweet_target_deleted'][0]:
                    tweet_err = self.error_code['tweet_target_deleted'][1]
                    self.api.update_status(status=tweet_err,
                                           in_reply_to_status_id=tweet.id,
                                           auto_populate_reply_metadata=True)
                    self.show_what_tweeted(tweet_err)

                elif error == self.error_code['tweet_target_to_long'][0]:
                    tweet_err = self.error_code['tweet_target_to_long'][1]
                    self.api.update_status(status=tweet_err,
                                           in_reply_to_status_id=tweet.id,
                                           auto_populate_reply_metadata=True)
                    self.show_what_tweeted(tweet_err)

                elif error == self.error_code['twitter_over_capacity'][0]:
                    tweet_err = self.error_code['twitter_over_capacity'][1]
                    self.api.update_status(status=tweet_err,
                                           in_reply_to_status_id=tweet.id,
                                           auto_populate_reply_metadata=True)
                    self.show_what_tweeted(tweet_err)

                elif error == self.error_code['suspended_account'][0]:
                    tweet_err = self.error_code['suspended_account'][1]
                    self.api.update_status(status=tweet_err,
                                           in_reply_to_status_id=tweet.id,
                                           auto_populate_reply_metadata=True)
                    self.show_what_tweeted(tweet_err)

                elif error == self.error_code['duplicate_tweet'][0]:
                    tweet_err = self.error_code['duplicate_tweet'][1]
                    self.show_what_tweeted(tweet_err)
                    continue

                elif error == self.error_code['tweet_deleted_or_not_visible'][0]:
                    tweet_err = self.error_code['tweet_deleted_or_not_visible'][1]
                    self.show_what_tweeted(tweet_err)

                elif error == self.error_code['page_does_not_exist'][0]:
                    tweet_err = self.error_code['page_does_not_exist'][1]
                    self.show_what_tweeted(tweet_err)

                else:
                    t = time.localtime()
                    current_time = time.strftime("%H:%M:%S %D", t)
                    db.select_col('tweet_error')
                    db.insert_object(
                        {'error_code': str(error),
                            'timestamp': current_time,
                            'tweet_id': tweet.id,
                            'username': tweet.user.screen_name,
                            'tweet_text': tweet.full_text,
                            'error_text': error_text})

            time.sleep(self.time_interval)
            continue

    def get_mention_tweet(self, since_id):
        new_since_id = since_id

        db = Database()
        db.connect_db('twitter')
        db.select_col('tweet')

        list_tweet = []

        for tweet in tweepy.Cursor(self.api.mentions_timeline, since_id=since_id, tweet_mode="extended").items():
            user_account_old = tweet.user.created_at.date()
            new_since_id = max(tweet.id, new_since_id)

            words = tweet.full_text.lower().split()
            if self.am_i_mentioned(tweet) == 'mockthistweet':
                if self.account_old(user_account_old) > 6:
                    fs = self.check_follower(self.my_bot_id, tweet.user.id)
                    if (fs[0].followed_by):
                        if since_id != tweet.id:
                            list_tweet.append(tweet)
                        print("account old: {}".format(self.account_old(user_account_old)),
                              tweet.id, 'added to next process')
                    else:
                        for tw in self.triggering_words:
                            if tw in words:
                                db.select_col('not_follower')
                                db.insert_object({'tweet_id': tweet.id,
                                                  'username': tweet.user.screen_name})
                                self.tweeted_and_show(
                                    self.tweet_text["follow_dulu"], tweet, 'back')
                        print("account old: {}".format(self.account_old(user_account_old)),
                              tweet.id, 'skipped not follower')

            elif self.am_i_mentioned(tweet) != 'mockthistweet':
                for tw in self.triggering_words:
                    if tw in words:
                        self.tweeted_and_show(
                            self.tweet_text["untag_dong"], tweet, 'back')

        self.process_mention(list_tweet)

        return new_since_id
