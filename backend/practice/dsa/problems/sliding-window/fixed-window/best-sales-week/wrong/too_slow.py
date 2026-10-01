class Solution:
    # Mistake: re-adds every window from scratch: O(n * k).
    def bestWeek(self, sales, k):
        best = None
        for i in range(len(sales) - k + 1):
            t = 0
            for v in sales[i:i + k]:
                t += v
            best = t if best is None else max(best, t)
        return best
