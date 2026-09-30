from ren_gen import ints
def small(rng):
    return {"first": sorted(ints(rng, rng.randint(0, 5), -5, 5)), "second": sorted(ints(rng, rng.randint(0, 5), -5, 5))}
def build(rng, a, b, hi=10**5):
    return {"first": sorted(ints(rng, a, -hi, hi)), "second": sorted(ints(rng, b, -hi, hi))}
