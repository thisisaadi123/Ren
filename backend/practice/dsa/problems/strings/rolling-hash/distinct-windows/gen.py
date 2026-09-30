from ren_gen import word
def small(rng):
    s = word(rng, rng.randint(1, 12), "abc"[:rng.randint(1, 3)])
    return {"s": s, "k": rng.randint(1, len(s))}
def build(rng, n, k, alpha="abc", shape="random"):
    if shape == "period":
        unit = word(rng, 7, alpha)
        s = (unit * n)[:n]
    else:
        s = word(rng, n, alpha)
    return {"s": s, "k": min(k, n)}
