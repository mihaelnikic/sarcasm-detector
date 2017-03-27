from historical_predictor.extractor import TwitterExtractor
import nltk
from nltk.tokenize import TweetTokenizer
from nltk.stem import PorterStemmer as ps

id = 240444474994618369
#nltk.download()
twt = TweetTokenizer()

extractor = TwitterExtractor(id)
extractor.load_tweet()
print(extractor.author)
print(extractor.text)
print(nltk.pos_tag(twt.tokenize(extractor.text)))
print(nltk.pos_tag(twt.tokenize('because Fox is well-balanced and objective')))
stemmer = ps()
print(nltk.pos_tag([stemmer.stem(word) for word in twt.tokenize('Fox\'s World Cup streaming options are terrible')]))
if True:
    exit(0)
extractor.load_historical_tweets(preprocessing=False)
for h_tweet in extractor.get_historical_tweets():
    #print(h_tweet)
    print(nltk.pos_tag(twt.tokenize(h_tweet[1])))
    break
