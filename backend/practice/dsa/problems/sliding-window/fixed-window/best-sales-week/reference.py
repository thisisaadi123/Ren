class Solution:
    def bestWeek(self, sales, k):
        total = sum(sales[:k])
        best = total
        for i in range(k, len(sales)):
            total += sales[i] - sales[i - k]
            best = max(best, total)
        return best
