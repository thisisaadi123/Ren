class Solution:
    def kthInGrid(self, grid, k):
        return sorted(x for row in grid for x in row)[k - 1]
