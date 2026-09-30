from ren_gen import word
def small(rng):
    return {"s": word(rng, rng.randint(1, 12), "ab1"[:rng.randint(1, 3)])}
def build(rng, n, alpha="abc", shape="random"):
    if shape == "same":
        return {"s": "7" * n}
    if shape == "two":
        half = n // 2
        a = word(rng, half // 2, alpha)
        b = word(rng, half // 2, alpha)
        return {"s": (a + a[::-1] + "x" + b + b[::-1])[:n]}
    return {"s": word(rng, n, alpha)}
