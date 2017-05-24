import shelve
import os.path
from predictor.predictor import Predictor


class PredictorWithStorage(Predictor):
    def __init__(self, base_predictor, store_file=None, save_to_store_file=True):
        self.save_to_store_file = save_to_store_file
        self.read_from_store_file = store_file is not None
        if self.read_from_store_file:
            self.store_file = store_file
        self.base_predictor = base_predictor
        self.predicted = None
        if self.read_from_store_file:
            self.fit_history = self.load_fit_history() #if os.path.exists(self.store_file) else {}
        else:
            self.fit_history = {}

    # def save_fit_history(self):
    #     #output_hist = open(self.store_file, 'wb')
    #     #pickle.dump(self.fit_history, output_hist)
    #     fit_history = shelve.open(self.store_file)
    #     fit_history.update(self.fit_history)
    #     #output_hist.close()

    def load_fit_history(self):
        #input_hist = open(self.store_file, 'rb')
        #fit_history = pickle.load(input_hist)
        fit_history = shelve.open(self.store_file)
        #input_hist.close()
        return fit_history

    def __del__(self):
        if self.read_from_store_file:
            self.fit_history.close()
    #     if self.read_from_store_file and self.save_to_store_file:
    #         self.save_fit_history()

    def fit(self, tweet_id):
        tweet_id = str(tweet_id)
        # If tweet does not exists
        if tweet_id not in self.fit_history:
            self.base_predictor.fit(tweet_id)
            self.fit_history[tweet_id] = self.predicted = self.base_predictor.predict()
        else:
            self.predicted = self.fit_history[tweet_id]

    def predict(self):
        return self.predicted
