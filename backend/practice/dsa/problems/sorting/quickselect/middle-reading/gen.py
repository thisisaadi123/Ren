from ren_gen import ints
def small(rng):
    return {"readings": ints(rng, 2 * rng.randint(0, 4) + 1, -5, 5)}
def build(rng, n, lo=-10**9, hi=10**9):
    return {"readings": ints(rng, n, lo, hi)}
