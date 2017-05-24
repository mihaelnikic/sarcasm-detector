from integrators.or_integrator import ORIntegrator
from integrators.and_integrator import ANDIntegrator
from integrators.only_hist_integrator import OnlyHistoricalTweetIntegrator
from integrators.relaxed_and_integrator import RelaxedANDIntegrator
from historical_predictor.h_predictor import HistoricPredictor
from contrast_predictor.c_predictor import ContrastPredictor
from predictor.predictor_with_storage import PredictorWithStorage

hist_predictor = PredictorWithStorage(HistoricPredictor(), store_file='/home/mihael/Documents/8. '
                                                                      'semestar/SEMINAR/git/Implementacija/predictor'
                                                                      '/stored_predictions/hist.shelve')
contrast_predictor = PredictorWithStorage(ContrastPredictor('/home/mihael/Documents/8. '
                                                            'semestar/SEMINAR/git/Implementacija/dataset'
                                                            '/Training dataset/grams/phrases.pkl')
                                          , store_file='/home/mihael/Documents/8. '
                                                       'semestar/SEMINAR/git/Implementacija/predictor'
                                                       '/stored_predictions/cont.shelve')
# AND integrator
and_integrator = ANDIntegrator(hist_predictor, contrast_predictor)
and_integrator.fit(240444474994618369)

# OR integrator
or_integrator = ORIntegrator(hist_predictor, contrast_predictor)
or_integrator.fit(240444474994618369)

# Only Historical tweet integrator
oHTI_integrator = OnlyHistoricalTweetIntegrator(hist_predictor)
oHTI_integrator.fit(240444474994618369)

# Relaxed AND integrator
relaxedAND_integrator = RelaxedANDIntegrator(hist_predictor, contrast_predictor)
relaxedAND_integrator.fit(240444474994618369)

print("AND integrator: " + str(and_integrator.predict()))
print("OR integrator: " + str(or_integrator.predict()))
print("Only Historical tweet-based predictor: " + str(oHTI_integrator.predict()))
print("RelaxedAND predictor: " + str(relaxedAND_integrator.predict()))
