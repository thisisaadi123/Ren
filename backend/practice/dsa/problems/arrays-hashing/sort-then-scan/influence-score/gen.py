from ren_gen import ints
def small(rng):
    return {"citations": ints(rng, rng.randint(1, 8), 0, 8)}
def build(rng, n, hi=0):
    return {"citations": ints(rng, n, 0, hi or n)}
