class Solution:
    # Mistake: starts the best total at 0, so an all-loss answer comes out as 0.
    def bestWeek(self, sales, k):
        total = sum(sales[:k])
        best = max(0, total)
        for i in range(k, len(sales)):
            total += sales[i] - sales[i - k]
            best = max(best, total)
        return best
