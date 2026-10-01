def build(rng, n, shape="random"):
    if shape == "nines":
        d = [9] * n
    elif shape == "tail":
        k = rng.randint(1, n)
        d = [rng.randint(0, 9) for _ in range(n - k)] + [9] * k
        if n - k:
            d[n - k - 1] = rng.randint(0, 8)
    else:
        d = [rng.choice((rng.randint(0, 9), 9)) for _ in range(n)]
    if d[0] == 0 and n > 1:
        d[0] = rng.randint(1, 9)
    return {"head": d}


def small(rng):
    return build(rng, rng.randint(1, 5), rng.choice(("random", "random", "nines", "tail")))
