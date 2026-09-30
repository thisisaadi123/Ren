from ren_gen import ints
def small(rng):
    p = ints(rng, rng.randint(1, 10), 0, rng.choice([2, 4, 6]))
    return {"plays": p, "k": rng.randint(1, len(set(p)))}
def build(rng, n, spread=50, k=0):
    p = ints(rng, n, -spread, spread)
    d = len(set(p))
    return {"plays": p, "k": min(d, k) if k else rng.randint(1, d)}
