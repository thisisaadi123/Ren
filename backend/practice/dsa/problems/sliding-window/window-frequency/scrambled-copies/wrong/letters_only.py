class Solution:
    # Mistake: checks only which letters appear, not how many of each.
    def scrambledCopies(self, text, word):
        m = len(word)
        need = set(word)
        return [i for i in range(len(text) - m + 1) if set(text[i:i + m]) == need]
