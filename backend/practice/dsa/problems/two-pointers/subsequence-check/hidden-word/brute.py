import itertools
class Solution:
    def isHidden(self, word, text):
        return any("".join(c) == word for c in itertools.combinations(text, len(word)))
