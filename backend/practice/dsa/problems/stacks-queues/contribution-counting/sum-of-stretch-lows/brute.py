class Solution:
    def sumOfLows(self, prices):
        n = len(prices)
        total = 0
        for i in range(n):
            low = prices[i]
            for j in range(i, n):
                low = min(low, prices[j])
                total += low
        return total % (10**9 + 7)
