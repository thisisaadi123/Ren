def small(rng):
    return {"head": sorted(rng.randint(-3, 3) for _ in range(rng.randint(0, 9)))}


def build(rng, n, shape="random", span=1000):
    if shape == "same":
        return {"head": [rng.randint(-10**6, 10**6)] * n}
    if shape == "distinct":
        return {"head": sorted(rng.sample(range(-10**6, 10**6 + 1), n))}
    if shape == "pairs":  # every value twice: the answer is empty
        vals = sorted(rng.sample(range(-10**6, 10**6 + 1), n // 2))
        return {"head": [v for v in vals for _ in (0, 1)]}
    return {"head": sorted(rng.randint(-span, span) for _ in range(n))}
