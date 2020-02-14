import tweepy
import os
import time
import yaml
from datetime import datetime
from dateutil import relativedelta
from generator import drawText
from kalimat import Kalimat
from emoji_generator import Emoji
from db_mongo import Database
from dict import error_code, tweet_text, file_meme, trigger_words


class Twitter:
    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret
        self.auth = self.authentication()
        self.api = tweepy.API(self.auth)
        self.me = self.api.me()
        self.triggering_words = trigger_words
        self.developer_id = 1012117785512558592
        self.bot_id = 1157825461277167616
        self.bot_test_id = 1182299095370629123
        self.error_code = self.load_dict(error_code)
        self.tweet_text = self.load_dict(tweet_text)
        self.file_meme = self.load_dict(file_meme)
        self.time_interval = 30
        self.db_name = os.environ.get("DB_NAME")

    def authentication(self):
        self.auth = tweepy.OAuthHandler(
            self.consumer_key, self.consumer_secret)
        self.auth.set_access_token(self.access_token, self.access_token_secret)
        return self.auth

    def load_dict(self, dict_name):
        dict = yaml.load("{}".format(dict_name), Loader=yaml.BaseLoader)
        return dict

    def check_follower(self, source_id, target_id):
        fs = self.api.show_friendship(source_id=source_id, target_id=target_id)
        return fs

    def get_account_old(self, user_old):
        today = datetime.now()
        diff = relativedelta.relativedelta(today, user_old)
        return diff.months+(diff.years*12)

    def show_what_tweeted(self, tweet_text):  # logger
        print(u"\u250C"+"-----------------------------------------------",
              "\n| tweeted 🐦", tweet_text,
              "\n| ", tweet_text,
              "\n"+u"\u2514"+"-----------------------------------------------")

    def show_status(self, tweet):
        print(u"\u250C"+"-----------------------------------------------",
              "\n| 👉: {} / {}".format(tweet.user.screen_name, tweet.user.id),
              "\n| tweet id: ", tweet.id,
              "\n| tweet: ", tweet.full_text,
              "\n"+u"\u2514"+"-----------------------------------------------")

    def tweeted_and_show(self, tweet_text, tweet, position):
        username = tweet.user.screen_name

        if position == 'back':
            tweet_text = tweet_text+username
        elif position == 'front':
            tweet_text = '@'+username+tweet_text
        elif position == 'format':
            tweet_text = tweet_text.format(username)

        try:
            self.api.update_status(status=tweet_text,
                                   in_reply_to_status_id=tweet.id,
                                   auto_populate_reply_metadata=True)
            self.show_what_tweeted(tweet_text)
        except tweepy.TweepError as e:
            print(e.api_code, e.response)
        time.sleep(self.time_interval)

    def tweet_mocked_tweet_picture(self, mocked_text, tweet_id, type):
        meme_type = None
        if type == 'spongebob':
            meme_type = 0
        else:
            meme_type = 1
        drawText(mocked_text, self.file_meme["input"][meme_type], type)
        self.api.update_with_media(filename=self.file_meme["output"][meme_type],
                                   status=mocked_text,
                                   in_reply_to_status_id=tweet_id,
                                   auto_populate_reply_metadata=True)
        self.show_what_tweeted(mocked_text)

    def mock_in_pliisi(self, tweet, db):
        tweet_target = self.api.get_status(tweet.in_reply_to_status_id,
                                           tweet_mode="extended")
        k = Kalimat(tweet_target.full_text)
        text_trinsfirmid = k.trinsfirm()
        self.tweet_mocked_tweet_picture(text_trinsfirmid, tweet.id, "khaleesi")
        db.insert_object({'tweet_last_id': tweet.id})

    def mock_in_please(self, tweet, db):
        tweet_target = self.api.get_status(tweet.in_reply_to_status_id,
                                           tweet_mode="extended")
        k = Kalimat(tweet_target.full_text)
        text_transformed = k.transform()
        self.tweet_mocked_tweet_picture(
            text_transformed, tweet.id, "spongebob")
        db.insert_object({'tweet_last_id': tweet.id})

    def mock_in_emoji(self, tweet, emoji_type, db):
        tweet_target = self.api.get_status(
            tweet.in_reply_to_status_id, tweet_mode="extended")
        k = Kalimat(tweet_target.full_text)

        if emoji_type == "laugh":
            text_transformoji = k.transformoji(emoji_type)

        elif emoji_type == "clap":
            text_transformoji = k.transformoji(emoji_type)

        elif emoji_type == "vomit":
            text_transformoji = k.transformoji(emoji_type)

        elif emoji_type == "sick":
            text_transformoji = k.transformoji(emoji_type)

        elif emoji_type == "poop":
            text_transformoji = k.transformoji(emoji_type)
            text_transformoji = "{} alias tai semua yg lo tweet".format(
                text_transformoji)

        self.api.update_status(status=text_transformoji,
                               in_reply_to_status_id=tweet.id,
                               auto_populate_reply_metadata=True)
        self.show_what_tweeted(text_transformoji)

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
            tweet_pattern = e.create_pattern(pattern)
            tweet_pattern += target_name

        elif pattern == 'b':
            text = "bisa diem gak {}, lo jelek".format(target_name)
            e = Emoji(text)
            re = e.random()
            e.pick_emoji(re)
            tweet_pattern = e.create_pattern(pattern)

        elif pattern == 'j':
            e = Emoji("jancok! raimu iku loh ")
            re = e.random()
            e.pick_emoji(re)
            tweet_pattern = e.create_pattern(pattern)
            tweet_pattern += target_name

        self.api.update_status(status=tweet_pattern,
                                in_reply_to_status_id=tweet.id,
                                auto_populate_reply_metadata=True)
        self.show_what_tweeted(tweet_pattern)

        db.insert_object({'tweet_last_id': tweet.id})

    def mock_in_alay(self, tweet, db):
        tweet_target = self.api.get_status(tweet.in_reply_to_status_id,
                                           tweet_mode="extended")
        k = Kalimat(tweet_target.full_text)
        text_transformed = k.transformalay()
        self.api.update_status(status=text_transformed,
                               in_reply_to_status_id=tweet.id,
                               auto_populate_reply_metadata=True)
        self.show_what_tweeted(text_transformed)
        db.insert_object({'tweet_last_id': tweet.id})

    def am_i_mentioned(self, tweet):
        for t in tweet.entities.items():
            for a in t[1]:
                last = list(a.items())[0][-1]
        return last

    def get_criteria(self, tweet):
        fs = self.check_follower(self.bot_id, tweet.user.id)
        user_account_old = tweet.user.created_at.date()
        reason = None

        is_follower = fs[0].followed_by
        is_old_enough = self.get_account_old(user_account_old) > 6

        is_elligible = is_follower and is_old_enough

        if is_follower:
            reason = 'not a follower'
        elif is_old_enough:
            reason = 'not old enough'
        else:
            reason = 'not in criteria'

        return is_elligible, reason

    def process_mention(self, list_tweet):
        db = Database()
        db.connect_db(self.db_name)
        db.select_col('tweet')

        for tweet in reversed(list_tweet):
            self.show_status(tweet)
            try:
                words = tweet.full_text.lower().split()
                if self.developer_id == tweet.in_reply_to_user_id:
                    for tw in self.triggering_words:
                        if tw in words:
                            self.tweeted_and_show(
                                self.tweet_text["dont_mock"][0], tweet, 'back')
                elif self.bot_id == tweet.in_reply_to_user_id or self.bot_test_id == tweet.in_reply_to_user_id:
                    continue
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

                        elif tw == "pleasealay" in words:
                            self.mock_in_alay(tweet, db)

                    time.sleep(self.time_interval)

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
            continue

    def get_mention_tweet(self, since_id):
        new_since_id = since_id

        db = Database()
        db.connect_db(self.db_name)
        db.select_col('tweet')

        list_tweet = []

        for tweet in tweepy.Cursor(self.api.mentions_timeline, since_id=since_id, tweet_mode="extended").items():
            new_since_id = max(tweet.id, new_since_id)
            words = tweet.full_text.lower().split()

            if self.am_i_mentioned(tweet) == self.me.screen_name:
                criteria = self.get_criteria(tweet)

                if criteria[0]:
                    if since_id != tweet.id:
                        for tw in self.triggering_words:
                            if tw in words:
                                list_tweet.append(tweet)
                    print('tweet id: {} added to next process'.format(tweet.id))
                else:
                    print('tweet id: {} skipped, reason: {}'.format(tweet.id, criteria[1]))

            elif self.am_i_mentioned(tweet) != self.me.screen_name:
                continue

        self.process_mention(list_tweet)

        return new_since_id
