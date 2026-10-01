def build(rng, n, k=0, kinds=0):
    labels = [rng.randint(1, 10**9) for _ in range(kinds or n)]
    return {"items": [rng.choice(labels) for _ in range(n)], "k": min(k or rng.randint(1, n), n)}


def small(rng):
    n = rng.randint(1, 8)
    return build(rng, n, rng.randint(1, n), rng.randint(1, 4))
