class Solution:
    # Mistake: needs more than h citations instead of at least h.
    def influenceScore(self, citations):
        s = sorted(citations, reverse=True)
        h = 0
        while h < len(s) and s[h] > h + 1:
            h += 1
        return h
