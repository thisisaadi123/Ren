def small(rng):
    n = rng.randint(1, 6)
    k = rng.randint(1, 4)
    vals = rng.sample(range(-10, 11), k)
    return {"coins": [rng.choice(vals) for _ in range(n)]}
def build(rng, n, k=4, shape="random"):
    if shape == "same":
        v = rng.randint(-10, 10)
        return {"coins": [v] * n}
    if shape == "distinct":
        return {"coins": rng.sample(range(-10, 11), n)}
    vals = rng.sample(range(-10, 11), k)
    return {"coins": [rng.choice(vals) for _ in range(n)]}
