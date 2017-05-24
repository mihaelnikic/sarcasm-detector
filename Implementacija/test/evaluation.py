import configparser
import sys
import pandas as pd
import pickle
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
from integrators.or_integrator import ORIntegrator
from integrators.and_integrator import ANDIntegrator
from integrators.only_hist_integrator import OnlyHistoricalTweetIntegrator
from integrators.relaxed_and_integrator import RelaxedANDIntegrator
from historical_predictor.h_predictor import HistoricPredictor
from contrast_predictor.c_predictor import ContrastPredictor
from predictor.predictor_with_storage import PredictorWithStorage


def precision_rec_f1(real, predicted):
    return "P = " + str(precision_score(real, predicted)) + ", R = " + str(
        recall_score(real, predicted)) + ", F = " + str(
        f1_score(real, predicted))


config = configparser.ConfigParser()
config.read(sys.argv[1])

# Load test set
test_set = pd.read_csv(config['dataset']['test'], sep=";", encoding='utf-8')

# Lists with real and map with predicted values
real = []
predicted = {key: [] for key in ['OHT', 'OR', 'AND', 'R-AND']}

# initalizing predictors
hist_predictor = PredictorWithStorage(HistoricPredictor(download_path=config['storage']['download_hist_tweets'],
                                                        # lexicon_file='/home/mihael/Documents/8. '
                                                        # 'semestar/SEMINAR/git/Implementacija/lexicon/L2/filtered/l2_lexicon_formatted.txt'
                                                        ),
                                      store_file=config['storage']['hist'])
contrast_predictor = PredictorWithStorage(ContrastPredictor(config['dataset']['phrases']
                                                            ,  # lexicon_file='/home/mihael/Documents/8. '
                                                            # 'semestar/SEMINAR/git/Implementacija/lexicon/L2/filtered/l2_lexicon_formatted.txt'
                                                            ),
                                          store_file=config['storage']['contrast'])

##initalizing integrators
and_integrator = ANDIntegrator(hist_predictor, contrast_predictor)
or_integrator = ORIntegrator(hist_predictor, contrast_predictor)
oHTI_integrator = OnlyHistoricalTweetIntegrator(hist_predictor)
relaxedAND_integrator = RelaxedANDIntegrator(hist_predictor, contrast_predictor)

# DEBUG
brojac = 0
limit = len(test_set)

for index, row in test_set.iterrows():
    tweet_id, sarcastic = row['tweet'], True if row['sentiment'] == 1 else False
    try:
        # AND integrator
        and_integrator.fit(tweet_id)
        predicted['AND'].append(and_integrator.predict())

        # OR integrator
        or_integrator.fit(tweet_id)
        predicted['OR'].append(or_integrator.predict())

        # Only Historical tweet integrator
        oHTI_integrator.fit(tweet_id)
        predicted['OHT'].append(oHTI_integrator.predict())

        # Relaxed AND integrator
        relaxedAND_integrator.fit(tweet_id)
        predicted['R-AND'].append(relaxedAND_integrator.predict())

        # DEBUG
        hist_predictor.fit(tweet_id)
        contrast_predictor.fit(tweet_id)

        real.append(sarcastic)
        brojac += 1
    except:
        print("FAIL - tweet not avaliable anymore: " + str(tweet_id))
        limit -= 1
    print(str(brojac) + "/" + str(limit) + " -> h: " + str(hist_predictor.predict()) + ", c: " + str(
        contrast_predictor.predict()) + ", REAL: " + str(sarcastic))
    if brojac >= limit:
        break

output_result = open('/home/mihael/Documents/8. semestar/SEMINAR/git/Implementacija/test/test_result.pkl', 'wb')
pickle.dump(predicted, output_result)
output_result.close()

# Print results
print("----------------------------")
print("Only historical tweet-based:")
print(precision_rec_f1(real, predicted['OHT']))
print("----------------------------")
print("OR")
print(precision_rec_f1(real, predicted['OR']))
print("----------------------------")
print("AND:")
print(precision_rec_f1(real, predicted['AND']))
print("----------------------------")
print("Relaxed-AND:")
print(precision_rec_f1(real, predicted['R-AND']))
