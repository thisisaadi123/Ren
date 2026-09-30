def small(rng):
    n = rng.randint(1, 9)
    return {"head": [rng.randint(-9, 9) for _ in range(n)], "k": rng.randint(1, n)}


def build(rng, n, k="random", shape="random"):
    head = list(range(n)) if shape == "ascending" else [rng.randint(-10**6, 10**6) for _ in range(n)]
    if k == "random":
        kk = rng.randint(1, n)
    elif k == "n":
        kk = n
    elif k == "half-plus":  # one full batch and a long leftover
        kk = n // 2 + 1
    else:
        kk = min(int(k), n)
    return {"head": head, "k": kk}
