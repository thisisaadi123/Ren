from ren_gen import ints
def small(rng):
    limit = rng.randint(3, 12)
    return {"weights": ints(rng, rng.randint(1, 8), 1, limit), "limit": limit}
def build(rng, n, limit=30000, lo=1):
    return {"weights": ints(rng, n, lo, limit), "limit": limit}
