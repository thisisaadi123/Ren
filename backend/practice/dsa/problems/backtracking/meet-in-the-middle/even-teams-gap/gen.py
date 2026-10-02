def build(rng, n=15, hi=10**7, neg=1):
    lo = -hi if neg else 0
    return {"skills": [rng.randint(lo, hi) for _ in range(2 * n)]}


def small(rng):
    return build(rng, rng.randint(1, 5), 20, rng.choice((0, 1)))
