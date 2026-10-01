class Solution:
    # Mistake: forgets the prices must all differ.
    def bestUniqueBundle(self, prices, k):
        total = sum(prices[:k])
        best = total
        for i in range(k, len(prices)):
            total += prices[i] - prices[i - k]
            best = max(best, total)
        return best
