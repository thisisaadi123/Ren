from ren_gen import ints
def make(rng, n, spread, hit):
    a = sorted(ints(rng, n, -spread, spread))
    k = rng.randrange(n)
    a = a[k:] + a[:k]
    return {"shelf": a, "target": rng.choice(a) if hit else rng.randint(-spread - 1, spread + 1)}
def small(rng):
    return make(rng, rng.randint(1, 8), rng.choice([1, 2, 5]), rng.random() < 0.5)
def build(rng, n, spread=10**4 - 1, hit=1):
    return make(rng, n, spread, bool(hit))
