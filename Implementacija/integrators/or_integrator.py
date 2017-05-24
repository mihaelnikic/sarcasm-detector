from integrators.integrator import Integrator


class ORIntegrator(Integrator):

    def __init__(self, hist_predictor, contrast_predictor):
        self.hist_predictor = hist_predictor
        self.contrast_predictor = contrast_predictor

    def fit(self, tweet_id):
        self.hist_predictor.fit(tweet_id)
        self.contrast_predictor.fit(tweet_id)

    def predict(self):
        return self.hist_predictor.predict() or self.contrast_predictor.predict()
