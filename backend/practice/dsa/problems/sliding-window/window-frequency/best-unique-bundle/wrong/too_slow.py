class Solution:
    # Mistake: checks every window from scratch: O(n * k).
    def bestUniqueBundle(self, prices, k):
        best = 0
        for i in range(len(prices) - k + 1):
            part = prices[i:i + k]
            if len(set(part)) == k:
                best = max(best, sum(part))
        return best
