from ren_gen import ints
def small(rng):
    return {"walls": ints(rng, rng.randint(1, 9), 0, 6)}
def build(rng, n, hi=100_000, shape="random"):
    w = ints(rng, n, 0, hi)
    if shape == "valley":
        w = sorted(w[: n // 2], reverse=True) + sorted(w[n // 2 :])
    elif shape == "mountain":
        w = sorted(w[: n // 2]) + sorted(w[n // 2 :], reverse=True)
    elif shape == "edges":
        w = [0] * n
        w[0] = w[-1] = hi
    return {"walls": w}
