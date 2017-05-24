from historical_predictor.twitter_extractor import TwitterExtractor
import nltk
from nltk.tag.sequential import ClassifierBasedTagger
import os
from nltk.tokenize import TweetTokenizer
from nltk.stem import PorterStemmer as ps

from nltk.tokenize import treebank

id = 240444474994618369
#nltk.download()
#twt = TweetTokenizer()

#extractor = TwitterExtractor(id)
#extractor.load_tweet()
#print(extractor.author)
#print(extractor.text)
#print(nltk.pos_tag(twt.tokenize(extractor.text)))
#print(nltk.pos_tag(twt.tokenize('because Fox is well-balanced and objective')))
#stemmer = ps()
#print(nltk.pos_tag([stemmer.stem(word) for word in twt.tokenize('Fox\'s World Cup streaming options are terrible')]))
#if True:
#    exit(0)
#extractor.load_historical_tweets(preprocessing=False)
POS_TAGGER = 'taggers/maxent_treebank_pos_tagger/english.pickle'
if False:
    extractor = TwitterExtractor(id)
    print(extractor.tt())
    exit(0)
extractor = TwitterExtractor(id)
extractor.load_tweet()
extractor.load_historical_tweets(download_mode='r')
i = 0

for h_tweet in extractor.get_historical_tweets():
    print("iter: " + str(i) + "---------------------------------------------------------")
    print(h_tweet)
    #print(extractor.get_text())
    tagger = nltk.load(POS_TAGGER)
    #print(tagger)
    #print(tagger.tag(h_tweet[1]))
    #print(nltk.pos_tag(h_tweet[1].split(' '))[0])
    #   print(nltk.pos_tag(twt.tokenize(h_tweet[1])))
    if i > 200:
        break
    else:
        i += 1


