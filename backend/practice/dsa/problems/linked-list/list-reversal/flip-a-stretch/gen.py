def small(rng):
    n = rng.randint(1, 8)
    a, b = sorted((rng.randint(1, n), rng.randint(1, n)))
    return {"head": [rng.randint(-9, 9) for _ in range(n)], "left": a, "right": b}


def build(rng, n, span="random"):
    head = [rng.randint(-10**5, 10**5) for _ in range(n)]
    if span == "all":
        a, b = 1, n
    elif span == "prefix":
        a, b = 1, rng.randint(1, n)
    elif span == "suffix":
        a, b = rng.randint(1, n), n
    elif span == "one":
        a = b = rng.randint(1, n)
    else:
        a, b = sorted((rng.randint(1, n), rng.randint(1, n)))
    return {"head": head, "left": a, "right": b}
