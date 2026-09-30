from ren_gen import ints
def small(rng):
    n, s = rng.randint(1, 4), rng.randint(1, 3)
    return {k: ints(rng, n, -s, s) for k in "abcd"}
def build(rng, n, spread=5):
    return {k: ints(rng, n, -spread, spread) for k in "abcd"}
