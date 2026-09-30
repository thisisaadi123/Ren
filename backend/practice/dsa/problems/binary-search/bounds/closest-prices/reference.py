class Solution:
    def closestPrices(self, prices, k, x):
        lo, hi = 0, len(prices) - k
        while lo < hi:
            mid = (lo + hi) // 2
            if x - prices[mid] > prices[mid + k] - x:
                lo = mid + 1
            else:
                hi = mid
        return prices[lo : lo + k]
