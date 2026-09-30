from ren_gen import ints
def two(rng, n, m, spread):
    return sorted(ints(rng, n, -spread, spread)), sorted(ints(rng, m, -spread, spread))

def small(rng):
    n, m = rng.randint(0, 5), rng.randint(0, 5)
    if n + m == 0:
        m = 1
    a, b = two(rng, n, m, 6)
    return {"a": a, "b": b, "k": rng.randint(1, n + m)}
def build(rng, n, m, spread=10**9, where="random"):
    a, b = two(rng, n, m, spread)
    k = {"first": 1, "last": n + m}.get(where) or rng.randint(1, n + m)
    return {"a": a, "b": b, "k": k}
