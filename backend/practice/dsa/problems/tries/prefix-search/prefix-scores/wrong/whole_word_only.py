class Solution:
    # Mistake: scores only the whole word, not every prefix.
    def prefixScores(self, words):
        return [sum(1 for x in words if x.startswith(w)) for w in words]
