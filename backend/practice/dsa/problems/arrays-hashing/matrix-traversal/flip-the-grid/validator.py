from ren_check import matrix
def validate(grid):
    matrix("grid", grid, 1, 1000, 1, 1000, -10**9, 10**9)
    assert len(grid) * len(grid[0]) <= 100_000, "m * n <= 10^5"
