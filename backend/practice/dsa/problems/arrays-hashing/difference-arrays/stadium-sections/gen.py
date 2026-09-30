def make(rng, n, m, wide):
    out = []
    for _ in range(m):
        if wide:
            l, r = rng.randint(0, n // 20), rng.randint(n - n // 20 - 1, n - 1)
        else:
            l = rng.randrange(n); r = rng.randint(l, min(n - 1, l + rng.randint(0, n)))
        out.append([l, r, rng.randint(1, 10**4)])
    return out
def small(rng):
    n = rng.randint(1, 6)
    return {"n": n, "groups": make(rng, n, rng.randint(1, 4), False)}
def build(rng, n, m, wide=0):
    return {"n": n, "groups": make(rng, n, m, bool(wide))}
