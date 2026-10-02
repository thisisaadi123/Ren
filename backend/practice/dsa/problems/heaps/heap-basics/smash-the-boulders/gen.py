def build(rng, n, hi=10**9):
    return {"boulders": [rng.randint(1, hi) for _ in range(n)]}


def small(rng):
    return build(rng, rng.randint(1, 8), rng.choice((3, 10, 100)))
