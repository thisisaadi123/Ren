class Solution:
    def cheapestPairs(self, a, b, k):
        return sorted(x + y for x in a for y in b)[:k]
