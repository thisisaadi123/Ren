from ren_check import ints, integer
def validate(a, b, k):
    ints("a", a, 0, 100_000, -10**9, 10**9)
    ints("b", b, 0, 100_000, -10**9, 10**9)
    assert all(x <= y for x, y in zip(a, a[1:])) and all(x <= y for x, y in zip(b, b[1:])), "both lists must be sorted"
    integer("k", k, 1, len(a) + len(b))
