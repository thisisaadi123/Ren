class Solution:
    def kthInGrid(self, grid, k):
        n = len(grid)

        def count_at_most(v):
            r, c, total = n - 1, 0, 0
            while r >= 0 and c < n:
                if grid[r][c] <= v:
                    total += r + 1
                    c += 1
                else:
                    r -= 1
            return total

        lo, hi = grid[0][0], grid[-1][-1]
        while lo < hi:
            mid = (lo + hi) // 2
            if count_at_most(mid) >= k:
                hi = mid
            else:
                lo = mid + 1
        return lo
