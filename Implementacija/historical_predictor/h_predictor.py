from historical_predictor.twitter_extractor import TwitterExtractor
from historical_predictor.pos_extractor import PosExtractor
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from predictor.predictor import Predictor
import numpy as np


class HistoricPredictor(Predictor):
    def __init__(self, lexicon_file=None, download_path=None):
        self.pos = PosExtractor()
        self.analyzer = SentimentIntensityAnalyzer() if lexicon_file is None else SentimentIntensityAnalyzer(
            lexicon_file=lexicon_file)
        self.predicted = None
        self.has_tweets = False
        self.download_path = download_path
        #DEBUG print
        self.debug_print = None

    def fit(self, tweet_id):
        # loading tweet and historical tweets

        self.has_tweets = False
        self.predicted = False
        extractor = TwitterExtractor(tweet_id)
        extractor.load_tweet()
        extractor.load_historical_tweets(download_path=self.download_path)

        self.debug_print = "h:" + str(tweet_id) + ";" + extractor.get_text().replace("\n", "\\n")
        # POS tagging tweet
        ht = extractor.get_historical_tweets()

        sentence_polarity = self.analyzer.polarity_scores(extractor.get_text())['compound']
        if sentence_polarity != 0:
            sentence_polarity = 1 if sentence_polarity > 0 else 0
            self.debug_print += ";tweet_polarity:" + ("POSITIVE" if sentence_polarity == 1 else "NEGATIVE")
        else:
            self.debug_print += ";tweet_polarity:None"
            with open("h_predictor_results.txt", "a") as myfile:
                myfile.write(self.debug_print + "\n")
            return self.has_tweets

        #for word in self.pos.extract_pos_tags(extractor.get_text(), 'NNP'):
            # print(word)
            # print(word + " -> " + str(ht[1][1]))
            #word_polarity = self.analyzer.polarity_scores(word)['compound']
            #if word_polarity == 0:
            #    continue
            #else:
            #    word_polarity = 1 if word_polarity > 0 else 0

        votes = []
        nnp_original = self.pos.extract_pos_tags(extractor.get_text(), 'NNP')
        self.debug_print += ";NNP:" + ";".join(nnp_original)
        for nnp in nnp_original:
            votes.clear()
            for h_tweet in ht:
            #nnp_list = self.pos.extract_pos_tags(h_tweet, 'NNP')
            #if any(word in h_tweet for word in nnp_original):#word in nnp_list:
            #for nnp in nnp_list:
                if nnp in h_tweet:
                    #polarity = sum(self.analyzer.polarity_scores(h_word)['compound'] for h_word in nnp_list) > 0
                    if h_tweet == extractor.get_text():
                        continue
                    polarity = self.analyzer.polarity_scores(h_tweet)['compound']
                    self.debug_print += ";h_tweet:" + h_tweet.replace("\n", "\\n")
                    if polarity != 0:
                        self.debug_print += ";tweet_polarity:" + ("POSITIVE" if sentence_polarity == 1 else "NEGATIVE")
                        #print("H_TWEET: " +  str(extractor.debug_map[h_tweet]) + " -> " + str(polarity)) #DEBUG
                        votes.append(1 if polarity > 0 else 0)
                    #DEBUG else
                    else:
                        self.debug_print += ";tweet_polarity:None"

            if len(votes) > 0:
                self.has_tweets = True
                self.predicted = True if np.argmax(np.bincount(votes)) != sentence_polarity else False
                if self.predicted:
                    break

        self.debug_print += ";predicted:" + str(self.predicted)
        with open("h_predictor_results.txt", "a") as myfile :
            myfile.write(self.debug_print + "\n")
        # For relaxedAND integrator
        return self.has_tweets

    def predict(self):
        return self.predicted

# DEBUG
hp = HistoricPredictor(download_path='/home/mihael/Documents/8. semestar/SEMINAR/git/Implementacija/historical_predictor/downloaded_tweets')
hp.fit(240400699110875136)
print(hp.predict())
