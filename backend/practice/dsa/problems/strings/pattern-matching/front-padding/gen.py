from ren_gen import word
def small(rng):
    return {"s": word(rng, rng.randint(0, 12), "abc"[:rng.randint(1, 3)])}
def build(rng, n, alpha="ab", shape="random"):
    if shape == "same":
        return {"s": "a" * n}
    if shape == "almost":
        return {"s": "a" * (n // 2) + "b" + "a" * (n - n // 2 - 1)}
    if shape == "pal-prefix":
        half = word(rng, n // 4, alpha)
        head = half + half[::-1]
        return {"s": head + word(rng, n - len(head), alpha)}
    return {"s": word(rng, n, alpha)}
