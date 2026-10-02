def build(rng, lo=1, hi=30, over=0):
    n = rng.randint(lo, hi)
    total = 3 << (n - 1)
    k = rng.randint(total + 1, total + 20) if over else rng.randint(1, min(total, 10**9))
    return {"n": n, "k": min(k, 10**9)}


def small(rng):
    return build(rng, 1, 8, rng.choice((0, 0, 1)))
