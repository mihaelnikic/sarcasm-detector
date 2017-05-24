from integrators.integrator import Integrator


class RelaxedANDIntegrator(Integrator):

    def __init__(self, hist_predictor, contrast_predictor):
        self.hist_predictor = hist_predictor
        self.contrast_predictor = contrast_predictor
        self.has_tweets = None

    def fit(self, tweet_id):
        self.has_tweets = self.hist_predictor.fit(tweet_id)
        self.contrast_predictor.fit(tweet_id)

    def predict(self):
        if self.has_tweets:
            return self.contrast_predictor.predict() and self.hist_predictor.predict()
        else:
            return self.contrast_predictor.predict()
