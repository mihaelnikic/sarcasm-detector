import twython as tw
import tweepy
from nltk.tokenize import TweetTokenizer
import re
import csv

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

    def load_tweet(self):
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

    def load_historical_tweets(self, silent=True, preprocessing=True):
        self.historical_loaded = True
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
        if not preprocessing:
            self.historical_tweets = [[tweet.id_str, tweet.text.encode("utf-8")] for tweet in alltweets]
        else:
            self.historical_tweets = [[tweet.id_str, self.preprocessor(tweet.text)] for tweet in
                                      alltweets]

    def get_historical_tweets(self):
        if not self.historical_loaded:
            raise Exception
        return self.historical_tweets

    @staticmethod
    def preprocessor(text):
        text = re.sub('<[^>]*>', '', text)
        text = re.sub('[\W]+', ' ', text.lower())
        #twt = TweetTokenizer()
        return
