class Solution:
    # Mistake: requires the letters to be next to each other.
    def isHidden(self, word, text):
        return word in text
