import abc


class Predictor:
    __metaclass__ = abc.ABCMeta

    @abc.abstractclassmethod
    def fit(self, tweet_id):
        pass

    @abc.abstractclassmethod
    def predict(self):
        pass
