class Solution:
    def prefixScores(self, words):
        return [sum(sum(1 for x in words if x.startswith(w[:i])) for i in range(1, len(w) + 1)) for w in words]
