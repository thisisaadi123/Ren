from ren_check import integer, edges
def validate(n, borders, m):
    integer("n", n, 1, 10)
    edges("borders", borders, n)
    integer("m", m, 1, 4)
