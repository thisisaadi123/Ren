class Solution:
    def blackout(self, grid):
        m, n = len(grid), len(grid[0])
        out = [row[:] for row in grid]
        for r in range(m):
            for c in range(n):
                if grid[r][c] == 0:
                    for k in range(n):
                        out[r][k] = 0
                    for k in range(m):
                        out[k][c] = 0
        return out
