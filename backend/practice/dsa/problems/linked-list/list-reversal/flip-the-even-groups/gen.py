def small(rng):
    return {"head": [rng.randint(0, 9) for _ in range(rng.randint(1, 12))]}


def build(rng, n, shape="random"):
    if shape == "ascending":
        return {"head": list(range(n))}
    return {"head": [rng.randint(0, 10**5) for _ in range(n)]}
