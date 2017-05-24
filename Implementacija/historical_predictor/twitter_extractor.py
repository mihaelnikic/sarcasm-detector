import twython as tw
import os.path
import tweepy
import pickle
import pprint
import re
from nltk.tokenize import TweetTokenizer

CONSUMER_KEY = "qGWa0auDtpVJXx1LaZQspsVWe"
CONSUMER_SECRET = "scSr5x4R1u7w7KAoQ47J8xG1J0nUozhpowzzjNPO2DYuD89plg"
OAUTH_TOKEN = "846031238813171713-5ywVPWAEPNDBlVnO6ReosjvAcTn5K3v"
OAUTH_TOKEN_SECRET = "1itTLCn9ytm6L0UNeHWObgaofsk4qE62cHyHvxSa1nBRH"


class TwitterExtractor:
    def __init__(self, tweet_id):
        self.tweet_id = tweet_id
        self.tweet_loaded = False
        self.historical_loaded = False
        self.text = None
        self.author = None
        self.historical_tweets = None
        self.twitter = None
        self.debug_map = {}
        self.dir = os.path.dirname(__file__)

    def load_tweet(self):
        if self.tweet_loaded:
            return None

        self.tweet_loaded = True
        self.twitter = tw.Twython(
            CONSUMER_KEY, CONSUMER_SECRET,
            OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

        tweet = self.twitter.show_status(id=self.tweet_id)
        self.text = tweet['text']
        self.author = tweet['user']['screen_name']

    def get_author(self):
        if not self.tweet_loaded:
            raise Exception
        return self.author

    def get_text(self):
        if not self.tweet_loaded:
            raise Exception
        return self.text

    def load_historical_tweets(self, silent=True, download_mode='r', download_path=None):
        if self.historical_loaded:
            return None

        if (download_mode is 'r' and download_path is not None) and (
                os.path.exists(os.path.join(download_path, 'hist_' + self.author + '.pkl'))):
            self.load_saved_tweets()
            self.historical_loaded = True
            return None

        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
        api = tweepy.API(auth)

        alltweets = []

        new_tweets = api.user_timeline(screen_name=self.author, count=200)

        alltweets.extend(new_tweets)

        oldest = alltweets[-1].id - 1

        while len(new_tweets) > 0:
            if not silent:
                print(u"getting tweets before {}".format(oldest))

            new_tweets = api.user_timeline(screen_name=self.author, count=200, max_id=oldest)

            alltweets.extend(new_tweets)

            oldest = alltweets[-1].id - 1
            if not silent:
                print(u"...{} tweets downloaded so far".format(len(alltweets)))

        self.historical_tweets = []
        for tweet in alltweets:
            if self.tweet_id != tweet.id:
                self.debug_map[tweet.text] = tweet.id
                self.historical_tweets.append(tweet.text)

        self.historical_loaded = True
        if download_mode is not 'w-' and download_path is not None:
            self.save_historical_tweets()

    def get_historical_tweets(self):
        if not self.historical_loaded:
            raise Exception
        return self.historical_tweets

    def save_historical_tweets(self):

        output_hist = open(os.path.join(self.dir, './downloaded_tweets/hist_' + self.author + '.pkl'), 'wb')
        pickle.dump(self.historical_tweets, output_hist)
        output_hist.close()

    def load_saved_tweets(self):

        input_hist = open(os.path.join(self.dir, './downloaded_tweets/hist_' + self.author + '.pkl'), 'rb')
        self.historical_tweets = pickle.load(input_hist)
        input_hist.close()

    # @staticmethod
    # def preprocessor(text):
    #     #tt = TweetTokenizer()
    #     #text = re.sub('<[^>]*>', '', text)
    #     #text = re.sub('[\W]+', ' ', text.lower())
    #     #return tt.tokenize(text)
    #     text = re.sub("#[^\s+]+", "", text)
    #     return re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", text).split()
    #
    # @staticmethod
    # def preprocessor_raw(text):
    #     text = re.sub("#[^\s+]+", "", text)
    #     return re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", text)