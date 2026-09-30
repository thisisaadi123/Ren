def small(rng):
    return {"head": [rng.randint(-9, 9) for _ in range(rng.randint(0, 7))]}


def build(rng, n, shape="random"):
    if shape == "same":
        return {"head": [7] * n}
    if shape == "ascending":
        return {"head": list(range(n))}
    return {"head": [rng.randint(-10**6, 10**6) for _ in range(n)]}
