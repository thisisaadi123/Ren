from ren_gen import ints
def small(rng):
    return {"values": sorted(ints(rng, rng.randint(1, 8), -6, 6))}
def build(rng, n, lo=-10**4, hi=10**4):
    return {"values": sorted(ints(rng, n, lo, hi))}
