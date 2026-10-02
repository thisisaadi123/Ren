def vocab(rng, count, lo, hi, alpha):
    return ["".join(rng.choice(alpha) for _ in range(rng.randint(lo, hi))) for _ in range(count)]


def build(rng, n, alpha="abc", lo=1, hi=8, shape="random"):
    if shape == "same":
        w = "".join(rng.choice(alpha) for _ in range(hi))
        return {"words": [w] * n}
    if shape == "nested":
        w = "".join(rng.choice(alpha) for _ in range(hi))
        return {"words": [w[:rng.randint(lo, hi)] for _ in range(n)]}
    return {"words": vocab(rng, n, lo, hi, alpha)}


def small(rng):
    return build(rng, rng.randint(1, 5), "ab", 1, 3, rng.choice(("random", "nested")))
