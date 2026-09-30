from ren_gen import ints
def small(rng):
    n = rng.randint(1, 8)
    return {"tickets": ints(rng, n, 1, n)}
def build(rng, n, shape="random"):
    if shape == "perm":
        t = list(range(1, n + 1)); rng.shuffle(t); return {"tickets": t}
    if shape == "same":
        return {"tickets": [rng.randint(1, n)] * n}
    return {"tickets": ints(rng, n, 1, n)}
