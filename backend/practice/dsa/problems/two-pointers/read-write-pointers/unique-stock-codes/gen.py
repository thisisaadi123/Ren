from ren_gen import ints
def small(rng):
    return {"codes": sorted(ints(rng, rng.randint(1, 8), -3, 3))}
def build(rng, n, lo=-10**4, hi=10**4):
    return {"codes": sorted(ints(rng, n, lo, hi))}
