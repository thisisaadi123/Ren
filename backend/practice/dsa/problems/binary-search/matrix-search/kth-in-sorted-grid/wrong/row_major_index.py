class Solution:
    # Mistake: assumes reading row by row gives sorted order.
    def kthInGrid(self, grid, k):
        n = len(grid)
        return grid[(k - 1) // n][(k - 1) % n]
