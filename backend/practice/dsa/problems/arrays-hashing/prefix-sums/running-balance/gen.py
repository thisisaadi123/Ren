from ren_gen import ints
def small(rng):
    return {"changes": ints(rng, rng.randint(1, 8), -5, 5)}
def build(rng, n, lo=-10**4, hi=10**4):
    return {"changes": ints(rng, n, lo, hi)}
