def build(rng, n, bits=31, shape="random"):
    if shape == "high":
        return {"nums": [rng.randrange(2**30, 2**31) for _ in range(n)]}
    if shape == "split":
        return {"nums": [rng.randrange(2**31) if rng.random() < 0.01 else rng.randrange(2**30) for _ in range(n)]}
    return {"nums": [rng.randrange(2**bits) for _ in range(n)]}


def small(rng):
    return build(rng, rng.randint(1, 8), rng.choice((3, 31)))
