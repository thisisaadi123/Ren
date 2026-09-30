class Solution:
    def countBigDrops(self, prices):
        n = len(prices)
        total = 0
        for i in range(n):
            for j in range(i + 1, n):
                if prices[i] > 2 * prices[j]:
                    total += 1
        return total
