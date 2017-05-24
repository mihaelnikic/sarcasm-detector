from integrators.integrator import Integrator


class OnlyHistoricalTweetIntegrator(Integrator):

    def __init__(self, hist_predictor):
        self.hist_predictor = hist_predictor

    def fit(self, tweet_id):
        self.hist_predictor.fit(tweet_id)

    def predict(self):
        return self.hist_predictor.predict()
