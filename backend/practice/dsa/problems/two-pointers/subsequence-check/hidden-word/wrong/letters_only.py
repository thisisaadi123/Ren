class Solution:
    # Mistake: checks the letters exist but ignores their order.
    def isHidden(self, word, text):
        return all(word.count(c) <= text.count(c) for c in set(word))
