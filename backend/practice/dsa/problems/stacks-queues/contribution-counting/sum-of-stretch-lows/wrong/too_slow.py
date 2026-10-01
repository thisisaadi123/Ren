class Solution:
    # Mistake: walks every stretch: O(n^2).
    def sumOfLows(self, prices):
        n = len(prices)
        total = 0
        for i in range(n):
            low = prices[i]
            for j in range(i, n):
                if prices[j] < low:
                    low = prices[j]
                total += low
        return total % (10**9 + 7)
