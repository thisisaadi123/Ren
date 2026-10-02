class WildcardDictionary:
    # Mistake: treats "." as an ordinary character.
    def __init__(self):
        self.words = set()

    def addWord(self, word):
        self.words.add(word)

    def search(self, pattern):
        return pattern in self.words
