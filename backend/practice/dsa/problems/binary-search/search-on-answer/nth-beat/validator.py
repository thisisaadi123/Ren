from ren_check import integer
def validate(n, a, b):
    integer("n", n, 1, 10**9)
    integer("a", a, 2, 40_000)
    integer("b", b, 2, 40_000)
