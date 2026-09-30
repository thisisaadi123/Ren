from ren_gen import ints
def small(rng):
    return {"a": sorted(ints(rng, rng.randint(1, 6), -20, 20)), "b": sorted(ints(rng, rng.randint(1, 6), -20, 20))}
def build(rng, n, m, hi=10**9, split=False):
    if split in (True, "true"):
        return {"a": sorted(ints(rng, n, -hi, -1)), "b": sorted(ints(rng, m, 1, hi))}
    return {"a": sorted(ints(rng, n, -hi, hi)), "b": sorted(ints(rng, m, -hi, hi))}
