def small(rng):
    return {"head": [rng.randint(-9, 9) for _ in range(rng.randint(1, 9))]}


def build(rng, n, shape="random"):
    if shape == "same":
        return {"head": [3] * n}
    return {"head": [rng.randint(-10**5, 10**5) for _ in range(n)]}
