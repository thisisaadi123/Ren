class Solution:
    # Mistake: treats "." as a letter.
    def countMatches(self, words, patterns):
        from collections import Counter
        c = Counter(words)
        return [c[p] for p in patterns]
