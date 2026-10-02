class PrefixTree:
    # Mistake: startsWith() only accepts prefixes that are themselves stored words.
    def __init__(self):
        self.words = set()

    def insert(self, word):
        self.words.add(word)

    def search(self, word):
        return word in self.words

    def startsWith(self, prefix):
        return prefix in self.words
