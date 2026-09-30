class Solution:
    # Mistake: looks for the first value with MORE than k cells at or below it (off by one).
    def kthInGrid(self, grid, k):
        n = len(grid)
        def count_at_most(v):
            return sum(bisect.bisect_right(row, v) for row in grid)
        lo, hi = grid[0][0], grid[-1][-1]
        while lo < hi:
            mid = (lo + hi) // 2
            if count_at_most(mid) > k:
                hi = mid
            else:
                lo = mid + 1
        return lo
