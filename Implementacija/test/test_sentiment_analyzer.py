from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score

NEGATIVE = 0
NEUTRAL = 2
POSITIVE = 4

analyzer = SentimentIntensityAnalyzer()


def calculate_polarity(compound):
    if compound == 0:
        return NEUTRAL
    return POSITIVE if compound > 0 else NEGATIVE


real = []
predicted = []

with open('/home/mihael/Documents/8. semestar/SEMINAR/git/Implementacija/test/sentiment140/testdata.manual.2009.06.14'
          '.csv') as file:
    for line in file:
        splitted = line.split(",")
        polarity = int(splitted[0].replace("\"", ""))
        text = splitted[5]
        real.append(polarity)
        predicted.append(calculate_polarity(analyzer.polarity_scores(text)['compound']))

print("Precision: " + str(precision_score(real, predicted, average='macro')))
