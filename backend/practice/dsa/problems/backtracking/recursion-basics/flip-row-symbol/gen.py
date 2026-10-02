def build(rng, lo=1, hi=60):
    n = rng.randint(lo, hi)
    return {"n": n, "k": rng.randint(1, 2 ** (n - 1))}


def small(rng):
    return build(rng, 1, 10)
