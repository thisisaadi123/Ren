from ren_check import integer
def validate(rows, cols, k):
    integer("rows", rows, 1, 30_000)
    integer("cols", cols, 1, 30_000)
    integer("k", k, 1, rows * cols)
