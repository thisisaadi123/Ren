import string
def small(rng):
    return {"s": "".join(rng.choice("abc"[:rng.randint(1, 3)]) for _ in range(rng.randint(1, 12)))}
def build(rng, n, k=26, shape="random"):
    alpha = string.ascii_lowercase[:k]
    if shape == "same":
        return {"s": "a" * n}
    if shape == "period":
        unit = "".join(rng.choice(alpha) for _ in range(k))
        return {"s": (unit * n)[:n]}
    return {"s": "".join(rng.choice(alpha) for _ in range(n))}
