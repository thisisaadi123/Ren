class Solution:
    def scrambledCopies(self, text, word):
        m = len(word)
        key = sorted(word)
        return [i for i in range(len(text) - m + 1) if sorted(text[i:i + m]) == key]
