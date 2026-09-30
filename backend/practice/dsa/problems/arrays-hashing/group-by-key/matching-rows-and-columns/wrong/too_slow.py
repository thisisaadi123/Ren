class Solution:
    def countMatchingPairs(self, grid):
        n = len(grid)
        total = 0
        for r in range(n):
            for c in range(n):
                total += all(grid[r][k] == grid[k][c] for k in range(n))
        return total
