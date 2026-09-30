from ren_gen import ints
def qs(rng, n, m, wide):
    out = []
    for _ in range(m):
        if wide:
            l, r = rng.randint(0, n // 10), rng.randint(n - n // 10 - 1, n - 1)
        else:
            l = rng.randrange(n); r = rng.randint(l, n - 1)
        out.append([l, r])
    return out
def small(rng):
    n = rng.randint(1, 6)
    return {"sales": ints(rng, n, -5, 5), "queries": qs(rng, n, rng.randint(1, 4), False)}
def build(rng, n, m, wide=0):
    return {"sales": ints(rng, n, -10**9, 10**9), "queries": qs(rng, n, m, bool(wide))}
