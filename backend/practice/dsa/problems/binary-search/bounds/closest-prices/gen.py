from ren_gen import ints
def make(rng, n, spread, k=None):
    a = sorted(ints(rng, n, -spread, spread))
    return {"prices": a, "k": k or rng.randint(1, n), "x": rng.randint(-spread - 2, spread + 2)}
def small(rng):
    return make(rng, rng.randint(1, 7), 5)
def build(rng, n, spread=10**9 - 2, k=0):
    return make(rng, n, spread, min(k, n) if k else None)
