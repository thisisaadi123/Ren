from ren_check import matrix, integer
def validate(rows, target):
    matrix("rows", rows, 1, 300, 1, 300, -10**9, 10**9)
    flat = [x for r in rows for x in r]
    assert all(a < b for a, b in zip(flat, flat[1:])), "read row by row, the grid must be strictly increasing"
    integer("target", target, -10**9, 10**9)
