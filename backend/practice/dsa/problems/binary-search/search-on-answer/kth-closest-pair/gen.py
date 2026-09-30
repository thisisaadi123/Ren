from ren_gen import ints
def small(rng):
    h = ints(rng, rng.randint(2, 8), 0, 20)
    n = len(h)
    return {"heights": h, "k": rng.randint(1, n * (n - 1) // 2)}
def build(rng, n, hi=10**6, where="random"):
    h = ints(rng, n, 0, hi)
    total = n * (n - 1) // 2
    k = {"first": 1, "last": total}.get(where) or rng.randint(1, total)
    return {"heights": h, "k": k}
