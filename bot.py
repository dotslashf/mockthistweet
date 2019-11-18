import tweepy
import os
import time
from dotenv import load_dotenv
from generator import drawText
from kalimat import Kalimat


class Twitter:
    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret
        self.auth = self.authentication()
        self.api = tweepy.API(self.auth)
        self.error_code = {
            "private_account": [179, "Inikan private account, mana bisa gue ngeliat tweetnya"],
            "blocked_account": [136, "Yah yang di mention ngeblock botnya"],
            "duplicate_tweet": [187, "Duplicated tweet"],
            "tweet_target_deleted": [144, "Tweetnya udah dihapus sama dong:("],
            "tweet_target_to_long": [186, "Tweetnya kepanjangan kalau di tambahin emoji, coba format yang lain"]
        }
        self.triggering_words = ["please", "pliisi", "please😂", "please👏"]
        self.my_user_id = 1012117785512558592
        self.my_bot_id = 1157825461277167616
        self.tweet_text = {
            "dont_mock": ["Gaboleh nge mock creator, jangan ngelawak deh ",
                          "Ya lu mau nyoba buat gue ngemock diri gue sendiri? Lucu banget lo "],
            "follow_dulu": "Udah pake bot gratis apa susahnya follow dulu sih, "
        }
        self.file_meme = {"output": ["img/meme_new_output.png", "img/meme_khaleesi_output.png"],
                          "input": ["img/meme_new.png", "img/meme_khaleesi.png"]}

    def authentication(self):
        self.auth = tweepy.OAuthHandler(
            self.consumer_key, self.consumer_secret)
        self.auth.set_access_token(self.access_token, self.access_token_secret)
        return self.auth

    def check_follower(self, source_id, target_id):
        fs = self.api.show_friendship(source_id=source_id, target_id=target_id)
        return fs

    def show_what_tweeted(self, tweet_text):  # logger
        print("------------------------------------------------",
              "\n|",
              "\n| tweeted: ", tweet_text,
              "\n| ",
              "\n------------------------------------------------")
        time.sleep(2)

    def show_status(self, tweet):
        print("------------------------------------------------",
              "\n| tweet id: ", tweet.id,
              "\n| username: ", tweet.user.screen_name,
              "\n| tweet: ", tweet.full_text,
              "\n------------------------------------------------\n")
        time.sleep(1)

    def follow_dulu_dong(self, tweet_text, tweet):
        self.api.update_status(status=tweet_text,
                               in_reply_to_status_id=tweet.id,
                               auto_populate_reply_metadata=True)
        self.show_what_tweeted(tweet_text)

    def dont_mock_the_bot(self, tweet_text, tweet):
        username = tweet.user.screen_name
        self.api.update_status(
            status=tweet_text+username, in_reply_to_status_id=tweet.id, auto_populate_reply_metadata=True)
        self.show_what_tweeted(tweet_text)

    def mock_in_pliisi(self, tweet):
        tweet_target = self.api.get_status(tweet.in_reply_to_status_id,
                                           tweet_mode="extended")
        k = Kalimat(tweet_target.full_text)
        text_trinsfirmid = k.trinsfirm()
        drawText(text_trinsfirmid, self.file_meme["input"][1])
        time.sleep(5)
        self.api.update_with_media(self.file_meme["output"][1],
                                   status=text_trinsfirmid, in_reply_to_status_id=tweet.id, auto_populate_reply_metadata=True)
        self.show_what_tweeted(text_trinsfirmid)

    def mock_in_please(self, tweet):
        tweet_target = self.api.get_status(tweet.in_reply_to_status_id,
                                           tweet_mode="extended")
        k = Kalimat(tweet_target.full_text)
        text_transformed = k.transform()
        drawText(text_transformed, self.file_meme["input"][0])
        time.sleep(5)
        self.api.update_with_media(self.file_meme["output"][0],
                                   status=text_transformed, in_reply_to_status_id=tweet.id, auto_populate_reply_metadata=True)
        self.show_what_tweeted(text_transformed)

    def mock_in_emoji(self, tweet, emoji_type):
        if emoji_type == "laugh":
            tweet_target = self.api.get_status(tweet.in_reply_to_status_id,
                                               tweet_mode="extended")
            k = Kalimat(tweet_target.full_text)
            text_transformoji = k.transformoji(emoji_type)
            self.api.update_status(status=text_transformoji,
                                   in_reply_to_status_id=tweet.id,
                                   auto_populate_reply_metadata=True)
            self.show_what_tweeted(text_transformoji)
            time.sleep(3)

        elif emoji_type == "clap":
            tweet_target = self.api.get_status(tweet.in_reply_to_status_id,
                                               tweet_mode="extended")
            k = Kalimat(tweet_target.full_text)
            text_transformoji = k.transformoji(emoji_type)
            self.api.update_status(status=text_transformoji,
                                   in_reply_to_status_id=tweet.id,
                                   auto_populate_reply_metadata=True)
            self.show_what_tweeted(text_transformoji)
            time.sleep(3)

    def get_mention_tweet(self, since_id):
        new_since_id = since_id

        for tweet in tweepy.Cursor(self.api.mentions_timeline, since_id=since_id, tweet_mode="extended").items():
            new_since_id = max(tweet.id, new_since_id)
            self.show_status(tweet)

            words = tweet.full_text.lower().split()

            try:
                for tw in self.triggering_words:
                    if tw == "pliisi" in words:
                        fs = self.check_follower(self.my_bot_id,
                                                 tweet.user.id)

                        if (fs[0].followed_by):
                            if self.my_user_id == tweet.in_reply_to_user_id:
                                self.dont_mock_the_bot(self.tweet_text["dont_mock"][0],
                                                       tweet)
                            elif self.my_bot_id == tweet.in_reply_to_user_id:
                                self.dont_mock_the_bot(self.tweet_text["dont_mock"][1],
                                                       tweet)
                            else:
                                self.mock_in_pliisi(tweet)
                        else:
                            self.follow_dulu_dong(self.tweet_text["follow_dulu"],
                                                  tweet)

                    elif tw == "please" in words:
                        fs = self.check_follower(self.my_bot_id,
                                                 tweet.user.id)

                        if (fs[0].followed_by):
                            if self.my_user_id == tweet.in_reply_to_user_id:
                                self.dont_mock_the_bot(self.tweet_text["dont_mock"][0],
                                                       tweet)
                            elif self.my_bot_id == tweet.in_reply_to_user_id:
                                self.dont_mock_the_bot(self.tweet_text["dont_mock"][1],
                                                       tweet)
                            else:
                                self.mock_in_please(tweet)
                        else:
                            self.follow_dulu_dong(self.tweet_text["follow_dulu"],
                                                  tweet)

                    elif tw == "please😂" in words:
                        fs = self.check_follower(self.my_bot_id,
                                                 tweet.user.id)

                        if (fs[0].followed_by):
                            if self.my_user_id == tweet.in_reply_to_user_id:
                                self.dont_mock_the_bot(self.tweet_text["dont_mock"][0],
                                                       tweet)
                            elif self.my_bot_id == tweet.in_reply_to_user_id:
                                self.dont_mock_the_bot(self.tweet_text["dont_mock"][1],
                                                       tweet)
                            else:
                                self.mock_in_emoji(tweet, "laugh")
                        else:
                            self.follow_dulu_dong(self.tweet_text["follow_dulu"],
                                                  tweet)

                    elif tw == "please👏" in words:
                        fs = self.check_follower(self.my_bot_id,
                                                 tweet.user.id)

                        if (fs[0].followed_by):
                            if self.my_user_id == tweet.in_reply_to_user_id:
                                self.dont_mock_the_bot(self.tweet_text["dont_mock"][0],
                                                       tweet)
                            elif self.my_bot_id == tweet.in_reply_to_user_id:
                                self.dont_mock_the_bot(self.tweet_text["dont_mock"][1],
                                                       tweet)
                            else:
                                self.mock_in_emoji(tweet, "clap")
                        else:
                            self.follow_dulu_dong(self.tweet_text["follow_dulu"],
                                                  tweet)
            except tweepy.TweepError as e:
                error = e.api_code

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

                elif error == self.error_code['duplicate_tweet'][0]:
                    tweet_err = self.error_code['duplicate_tweet'][1]
                    self.show_what_tweeted(tweet_err)

                else:
                    print(error)
                    tweet_err = "error code: "+str(error)
                    self.api.update_status(status=tweet_err,
                                           in_reply_to_status_id=tweet.id,
                                           auto_populate_reply_metadata=True)
                    self.show_what_tweeted(tweet_err)

                continue

        return new_since_id
