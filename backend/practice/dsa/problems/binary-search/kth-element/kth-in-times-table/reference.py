class Solution:
    def kthInTable(self, rows, cols, k):
        if rows > cols:
            rows, cols = cols, rows
        lo, hi = 1, rows * cols
        while lo < hi:
            mid = (lo + hi) // 2
            if sum(min(mid // i, cols) for i in range(1, rows + 1)) >= k:
                hi = mid
            else:
                lo = mid + 1
        return lo
