class Solution:
    # Mistake: swaps in place, which only works for square grids.
    def transpose(self, grid):
        n = len(grid)
        for r in range(n):
            for c in range(r + 1, min(n, len(grid[0]))):
                grid[r][c], grid[c][r] = grid[c][r], grid[r][c]
        return grid
