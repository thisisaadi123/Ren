from ren_check import ints
def validate(a, b):
    ints("a", a, 0, 100_000, -10**6, 10**6)
    ints("b", b, 0, 100_000, -10**6, 10**6)
    assert len(a) + len(b) >= 1, "at least one waiting time"
    assert all(x <= y for x, y in zip(a, a[1:])) and all(x <= y for x, y in zip(b, b[1:])), "both lists must be sorted"
