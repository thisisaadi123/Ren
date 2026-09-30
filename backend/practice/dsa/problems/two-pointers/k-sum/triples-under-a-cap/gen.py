from ren_gen import ints
def small(rng):
    return {"values": ints(rng, rng.randint(3, 7), -5, 5), "cap": rng.randint(-10, 10)}
def build(rng, n, hi=10**4, cap=None):
    return {"values": ints(rng, n, -hi, hi), "cap": cap if cap is not None else rng.randint(-3 * hi, 3 * hi)}
