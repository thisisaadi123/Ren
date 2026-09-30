class Solution:
    # Mistake: treats the grid like a seat map and only searches one row.
    def inWarehouse(self, grid, target):
        firsts = [r[0] for r in grid]
        i = bisect.bisect_right(firsts, target) - 1
        if i < 0:
            return False
        row = grid[i]
        j = bisect.bisect_left(row, target)
        return j < len(row) and row[j] == target
