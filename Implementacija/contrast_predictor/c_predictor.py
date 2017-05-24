from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from contrast_predictor.pkl_phrase_finder import SerializedPhraseFinder
from nltk.tokenize import TweetTokenizer
from historical_predictor.twitter_extractor import TwitterExtractor
from predictor.predictor import Predictor


class ContrastPredictor(Predictor):
    def __init__(self, implicit_phrases_path, lexicon_file=None):
        self.analyzer = SentimentIntensityAnalyzer() if lexicon_file is None else SentimentIntensityAnalyzer(
            lexicon_file=lexicon_file)
        self.tokenizer = TweetTokenizer()
        self.phrase_finder = SerializedPhraseFinder(implicit_phrases_path)
        self.predicted = None
        # DEBUG print
        self.debug_print = None

    def fit(self, tweet_id):
        # loading tweet and historical tweets
        self.predicted = False
        extractor = TwitterExtractor(tweet_id)
        extractor.load_tweet()
        self.debug_print = "c:" + str(tweet_id) + ";" + extractor.get_text().replace("\n", "\\n")
        # print(extractor.get_text())
        has_positive, has_negative = self.fit_explicit(extractor)
        if self.predicted is not True:
            self.fit_implicit(extractor.get_text(), has_positive, has_negative)
        # DEBUG print
        self.debug_print += ";predicted:" + str(self.predicted)
        with open("c_predictor_results.txt", "a") as myfile:
            myfile.write(self.debug_print + "\n")

    def fit_explicit(self, extractor):
        has_p = False
        has_n = False
        self.debug_print += ";explicit:"
        for w in self.tokenizer.tokenize(extractor.get_text()):
            score = self.analyzer.polarity_scores(w)['compound']
            if score > 0:
                # print(w + " -> " + str(score))
                self.debug_print += ";" + w + ":POSITIVE"
                has_p = True
                if has_n:
                    self.predicted = True
                    break
            elif score < 0:
                # print(w + " -> " + str(score))
                self.debug_print += ";" + w + ":NEGATIVE"
                has_n = True
                if has_p:
                    self.predicted = True
                    break

        return has_p, has_n

    def fit_implicit(self, tweet, has_p, has_n):
        # Find all phrases that exist in a given tweet
        self.phrase_finder.find(tweet)
        self.debug_print += ";implicit:"
        # Extract sentiment from phrases
        for phrase in self.phrase_finder.retrieve():
            score = self.analyzer.polarity_scores(phrase)['compound']
            if score > 0:
                # print(phrase + " -> " + str(score))
                self.debug_print += ";" + phrase + ":POSITIVE"
                has_p = True
                if has_n:
                    self.predicted = True
                    break
            elif score < 0:
                # print(phrase + " -> " + str(score))
                self.debug_print += ";" + phrase + ":NEGATIVE"
                has_n = True
                if has_p:
                    self.predicted = True
                    break

    def predict(self):
        return self.predicted


# cp = ContrastPredictor('/home/mihael/Documents/8. semestar/SEMINAR/git/Implementacija/dataset/Training '
#                        'dataset/grams/phrases.pkl')
# cp.fit(241457865481662464)
# print(cp.predict())
