class Solution:
    def inWarehouse(self, grid, target):
        return any(target in row for row in grid)
