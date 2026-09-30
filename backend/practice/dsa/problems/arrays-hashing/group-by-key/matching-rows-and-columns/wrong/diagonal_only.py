class Solution:
    # Mistake: only compares row i with column i.
    def countMatchingPairs(self, grid):
        n = len(grid)
        return sum(list(grid[i]) == [grid[k][i] for k in range(n)] for i in range(n))
