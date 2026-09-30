from ren_gen import ints
def small(rng):
    a, b = rng.randint(0, 5), rng.randint(0, 5)
    if a + b == 0:
        a = 1
    return {"left": sorted(ints(rng, a, -5, 5)), "right": sorted(ints(rng, b, -5, 5))}
def build(rng, a, b, hi=10**9):
    return {"left": sorted(ints(rng, a, -hi, hi)), "right": sorted(ints(rng, b, -hi, hi))}
