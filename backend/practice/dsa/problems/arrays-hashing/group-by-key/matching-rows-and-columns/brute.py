class Solution:
    def countMatchingPairs(self, grid):
        n = len(grid)
        return sum(all(grid[r][k] == grid[k][c] for k in range(n)) for r in range(n) for c in range(n))
