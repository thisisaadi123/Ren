from ren_gen import ints
def small(rng):
    return {"grades": ints(rng, rng.randint(1, 9), 0, 100)}
def build(rng, n, lo=0, hi=100):
    return {"grades": ints(rng, n, lo, hi)}
