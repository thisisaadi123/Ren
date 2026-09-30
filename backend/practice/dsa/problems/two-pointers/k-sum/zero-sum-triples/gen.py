from ren_gen import ints
def small(rng):
    return {"values": ints(rng, rng.randint(3, 8), -4, 4)}
def build(rng, n, hi=10**5):
    return {"values": ints(rng, n, -hi, hi)}
