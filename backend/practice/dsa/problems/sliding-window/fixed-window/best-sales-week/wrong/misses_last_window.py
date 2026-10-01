class Solution:
    # Mistake: stops one step early and never looks at the last window.
    def bestWeek(self, sales, k):
        total = sum(sales[:k])
        best = total
        for i in range(k, len(sales) - 1):
            total += sales[i] - sales[i - k]
            best = max(best, total)
        return best
