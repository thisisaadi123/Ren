from ren_gen import ints
def small(rng):
    lo = rng.randint(-4, 4)
    return {"nums": ints(rng, rng.randint(1, 8), -4, 4), "lower": lo, "upper": rng.randint(lo, 5)}
def build(rng, n, spread=100, width=50):
    lo = rng.randint(-width, width)
    return {"nums": ints(rng, n, -spread, spread), "lower": lo, "upper": min(10**5, lo + rng.randint(0, width))}
