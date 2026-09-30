from ren_check import matrix, integer
def validate(grid, target):
    matrix("grid", grid, 1, 1000, 1, 1000, -10**9, 10**9)
    assert all(a <= b for row in grid for a, b in zip(row, row[1:])), "rows must be sorted"
    assert all(grid[i][j] <= grid[i + 1][j] for i in range(len(grid) - 1) for j in range(len(grid[0]))), "columns must be sorted"
    integer("target", target, -10**9, 10**9)
