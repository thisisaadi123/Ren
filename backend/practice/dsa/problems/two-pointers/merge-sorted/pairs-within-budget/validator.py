from ren_check import ints, integer
def validate(mains, sides, budget):
    for name, v in (("mains", mains), ("sides", sides)):
        ints(name, v, 1, 100_000, 1, 10**9)
        assert all(v[i] <= v[i + 1] for i in range(len(v) - 1)), "%s must be sorted" % name
    integer("budget", budget, 1, 2 * 10**9)
