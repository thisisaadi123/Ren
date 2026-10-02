class WildcardDictionary:
    # Mistake: accepts a pattern that matches only the start of a longer word.
    def __init__(self):
        self.words = []

    def addWord(self, word):
        self.words.append(word)

    def search(self, pattern):
        return any(len(w) >= len(pattern) and all(p == "." or p == c for p, c in zip(pattern, w)) for w in self.words)
