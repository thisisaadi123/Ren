class Solution:
    def blackout(self, grid):
        rows = {r for r, row in enumerate(grid) if 0 in row}
        cols = {c for c in range(len(grid[0])) if any(row[c] == 0 for row in grid)}
        for r, row in enumerate(grid):
            for c in range(len(row)):
                if r in rows or c in cols:
                    row[c] = 0
        return grid
