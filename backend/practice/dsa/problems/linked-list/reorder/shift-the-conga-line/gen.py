def small(rng):
    n = rng.randint(0, 7)
    return {"head": [rng.randint(-9, 9) for _ in range(n)], "k": rng.randint(0, 20)}


def build(rng, n, k="random"):
    head = [rng.randint(-10**6, 10**6) for _ in range(n)]
    if k == "random":
        kk = rng.randint(0, 2 * 10**9)
    elif k == "half":
        kk = n // 2 + n * rng.randint(0, 1000)
    elif k == "multiple":
        kk = n * (2 * 10**9 // max(n, 1))
    else:
        kk = int(k)
    return {"head": head, "k": kk}
