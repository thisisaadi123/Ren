from ren_check import ints
def validate(a, b):
    for name, v in (("a", a), ("b", b)):
        ints(name, v, 1, 100_000, -10**9, 10**9)
        assert all(v[i] <= v[i + 1] for i in range(len(v) - 1)), "%s must be sorted" % name
