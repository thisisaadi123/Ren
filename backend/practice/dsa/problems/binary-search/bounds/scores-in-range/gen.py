from ren_gen import ints
def make(rng, n, m, spread):
    qs = []
    for _ in range(m):
        a, b = rng.randint(-spread, spread), rng.randint(-spread, spread)
        qs.append([min(a, b), max(a, b)])
    return {"scores": ints(rng, n, -spread, spread), "queries": qs}
def small(rng):
    return make(rng, rng.randint(1, 7), rng.randint(1, 4), 5)
def build(rng, n, m, spread=10**9):
    return make(rng, n, m, spread)
