class Solution:
    def inWarehouse(self, grid, target):
        r, c = 0, len(grid[0]) - 1
        while r < len(grid) and c >= 0:
            v = grid[r][c]
            if v == target:
                return True
            if v > target:
                c -= 1
            else:
                r += 1
        return False
