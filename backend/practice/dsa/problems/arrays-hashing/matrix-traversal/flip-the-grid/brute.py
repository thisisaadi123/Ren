class Solution:
    def transpose(self, grid):
        m, n = len(grid), len(grid[0])
        out = [[0] * m for _ in range(n)]
        for r in range(m):
            for c in range(n):
                out[c][r] = grid[r][c]
        return out
