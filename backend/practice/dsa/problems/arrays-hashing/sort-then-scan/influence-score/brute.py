class Solution:
    def influenceScore(self, citations):
        return max(h for h in range(len(citations) + 1) if sum(c >= h for c in citations) >= h)
