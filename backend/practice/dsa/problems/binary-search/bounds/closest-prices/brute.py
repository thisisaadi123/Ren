class Solution:
    def closestPrices(self, prices, k, x):
        return sorted(sorted(prices, key=lambda p: (abs(p - x), p))[:k])
