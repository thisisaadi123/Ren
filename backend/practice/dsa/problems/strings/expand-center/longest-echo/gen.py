from ren_gen import word
def small(rng):
    return {"s": word(rng, rng.randint(1, 12), "abc"[:rng.randint(1, 3)])}
def build(rng, n, alpha="abc", shape="random"):
    if shape == "same":
        return {"s": "a" * n}
    if shape == "mirror":
        half = word(rng, n // 2, alpha)
        return {"s": half + half[::-1] + ("z" if n % 2 else "")}
    return {"s": word(rng, n, alpha)}
