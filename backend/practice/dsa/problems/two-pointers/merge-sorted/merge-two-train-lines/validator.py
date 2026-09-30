from ren_check import ints
def validate(first, second):
    for name, a in (("first", first), ("second", second)):
        ints(name, a, 0, 50_000, -10**5, 10**5)
        assert all(a[i] <= a[i + 1] for i in range(len(a) - 1)), "%s must be sorted" % name
