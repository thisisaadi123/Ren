class Solution:
    # Mistake: zeroes as it scans, so new zeros spread further.
    def blackout(self, grid):
        m, n = len(grid), len(grid[0])
        for r in range(m):
            for c in range(n):
                if grid[r][c] == 0:
                    for k in range(n):
                        grid[r][k] = 0
                    for k in range(m):
                        grid[k][c] = 0
        return grid
