

class SimplePhraseFinder:

    def __init__(self):
        self.o = open('phrases.txt')
        self.founded = []
        pass

    def find(self, tweet):
        self.founded.clear()
        for l in self.o:
            o = l.strip()
            if o in tweet:
                self.founded.append(o)

    def retrieve(self):
        return self.founded

sf = SimplePhraseFinder()
sf.find("RT   isRight  Good to see we have civil  impartial media in America")
print(sf.retrieve())