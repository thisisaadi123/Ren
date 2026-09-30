from ren_gen import ints
def small(rng):
    lo = rng.randint(-8, 8)
    return {"values": ints(rng, rng.randint(3, 7), -4, 4), "low": lo, "high": lo + rng.randint(0, 6)}
def build(rng, n, hi=10**6, width=None):
    v = ints(rng, n, -hi, hi)
    width = width if width is not None else rng.randint(0, 3 * hi)
    low = rng.randint(-3 * hi, 3 * hi - width)
    return {"values": v, "low": low, "high": low + width}
