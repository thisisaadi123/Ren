from ren_gen import ints


def build(rng, n, k=0, hi=10**4, limit=-1):
    k = min(k or rng.randint(1, n), n)
    a = ints(rng, n, 0, hi)
    if limit < 0:
        limit = rng.randint(0, hi)
    return {"noise": a, "k": k, "limit": min(limit, 10**4)}


def small(rng):
    n = rng.randint(1, 8)
    return build(rng, n, rng.randint(1, n), rng.choice((3, 10)))
