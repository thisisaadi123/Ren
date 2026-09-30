from ren_check import matrix, integer
def validate(grid, k):
    matrix("grid", grid, 1, 300, 1, 300, -10**9, 10**9)
    n = len(grid)
    assert len(grid[0]) == n, "grid must be square"
    assert all(a <= b for row in grid for a, b in zip(row, row[1:])), "rows must be sorted"
    assert all(grid[i][j] <= grid[i + 1][j] for i in range(n - 1) for j in range(n)), "columns must be sorted"
    integer("k", k, 1, n * n)
