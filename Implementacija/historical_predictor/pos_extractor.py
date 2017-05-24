import nltk
import historical_predictor.twokenize as twokenize
from historical_predictor.twitter_extractor import TwitterExtractor
#DEBUG
from nltk.classify.maxent import MaxentClassifier
from nltk import pos_tag, word_tokenize

POS_TAGGER = 'taggers/maxent_treebank_pos_tagger/english.pickle'


class PosExtractor:
    def __init__(self, source=POS_TAGGER):
        self.tagger = nltk.load(source)
        self.tokenizer = nltk.tokenize.TweetTokenizer()

    def extract_pos_tags(self, tweet, pos_tag):
        list = []
        tagged = self.tagger.tag(self.tokenizer.tokenize(tweet))

        sequence = None
        for t in tagged:
            if t[1].startswith(pos_tag):
                if sequence is None:
                    sequence = t[0]
                else:
                    sequence += " " + t[0]
            elif sequence is not None:
                list.append(sequence)
                sequence = None
        # check if last entry was sequence
        if sequence is not None:
            list.append(sequence)

        return list


# tweet = "I just love missing the bus"
# tweet2 = ['I just', 'just love', 'love missing', 'missing the', 'the bus']
# tweet3 = ['I just love', 'just love missing', 'love missing the', 'missing the bus']
# pe = PosExtractor()
# print(pos_tag(word_tokenize(tweet)))
# #print(tweet)
# print(pe.extract_pos_tags(tweet.split(), 'NNP'))
