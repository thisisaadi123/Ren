from ren_gen import word
def small(rng):
    return {"s": word(rng, rng.randint(1, 12), "abc"[:rng.randint(1, 3)])}
def build(rng, n, alpha="abc", shape="random"):
    if shape == "same":
        return {"s": "a" * n}
    if shape == "alt":
        return {"s": ("ab" * n)[:n]}
    if shape == "blocks":
        out = []
        while len(out) < n:
            out.extend(rng.choice(alpha) * rng.randint(1, 50))
        return {"s": "".join(out[:n])}
    return {"s": word(rng, n, alpha)}
