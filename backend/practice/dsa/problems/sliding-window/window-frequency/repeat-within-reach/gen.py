def build(rng, n, k=-1, gap=0):
    if gap:
        # Every value repeats exactly `gap` positions later and never closer.
        base = rng.sample(range(-10**9, 10**9), gap)
        a = [base[i % gap] for i in range(n)]
    else:
        a = rng.sample(range(-10**9, 10**9), n)
    return {"codes": a, "k": k if k >= 0 else rng.randint(0, n)}


def small(rng):
    n = rng.randint(1, 8)
    if rng.random() < 0.5:
        return {"codes": [rng.randint(0, 3) for _ in range(n)], "k": rng.randint(0, n)}
    return build(rng, n, rng.randint(0, n), rng.randint(0, n))
