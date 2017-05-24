import pickle
import re


class SerializedPhraseFinder:
    def __init__(self, file_path):
        self.phrases = self.load_pkl(file_path)
        self.founded = []
        pass

    @staticmethod
    def preprocessor(text):
        text = re.sub("#[^\s+]+", "", text)
        return re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", text)

    @staticmethod
    def load_pkl(file_path):
        input_phrases = open(file_path, 'rb')
        phrases = pickle.load(input_phrases)
        input_phrases.close()
        return phrases

    def find(self, tweet):
        self.founded.clear()
        for phrase_untrimmed in self.phrases:
            phrase = phrase_untrimmed.strip()
            if phrase in self.preprocessor(tweet):
                self.founded.append(phrase)

    def retrieve(self):
        return self.founded


#spf = SerializedPhraseFinder(
#    '/home/mihael/Documents/8. semestar/SEMINAR/git/Implementacija/dataset/Training dataset/grams/phrases.pkl')
#spf.find("It s a beautiful day, and I'm here too, If you re so ..., makes me feel ok")
#print(spf.retrieve())
