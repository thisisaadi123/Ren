from ren_check import ints
def validate(left, right):
    ints("left", left, 0, 100_000, -10**9, 10**9)
    ints("right", right, 0, 100_000, -10**9, 10**9)
    assert left or right, "at least one shelf must have a book"
    for name, a in (("left", left), ("right", right)):
        assert all(a[i] <= a[i + 1] for i in range(len(a) - 1)), "%s must be sorted" % name
