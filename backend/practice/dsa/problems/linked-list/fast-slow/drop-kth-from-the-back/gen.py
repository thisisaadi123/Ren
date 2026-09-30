def small(rng):
    n = rng.randint(1, 8)
    return {"head": [rng.randint(-9, 9) for _ in range(n)], "k": rng.randint(1, n)}


def build(rng, n, k="random"):
    head = [rng.randint(-10**6, 10**6) for _ in range(n)]
    kk = {"first": n, "last": 1, "random": rng.randint(1, n)}.get(k)
    if kk is None:
        kk = min(int(k), n)
    return {"head": head, "k": kk}
