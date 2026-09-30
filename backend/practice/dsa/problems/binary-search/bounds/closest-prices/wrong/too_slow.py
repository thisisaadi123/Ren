class Solution:
    def closestPrices(self, prices, k, x):
        chosen = []
        left = list(prices)
        for _ in range(k):
            best = min(left, key=lambda p: (abs(p - x), p))
            left.remove(best)
            chosen.append(best)
        return sorted(chosen)
