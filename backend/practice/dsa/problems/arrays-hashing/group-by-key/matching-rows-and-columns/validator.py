from ren_check import matrix
def validate(grid):
    matrix("grid", grid, 1, 600, 1, 600, 1, 100_000)
    assert len(grid[0]) == len(grid), "grid must be square"
