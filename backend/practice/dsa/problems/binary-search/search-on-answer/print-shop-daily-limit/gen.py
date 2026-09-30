def small(rng):
    """Random inputs small enough for brute.py."""
    n = rng.randint(1, 8)
    top = rng.choice([3, 10, 500])
    pages = [rng.randint(1, top) for _ in range(n)]
    return {"pages": pages, "days": rng.randint(1, n)}


def build(rng, n, shape="uniform", days="random"):
    """Recipe tests: --n <size> --shape <shape> --days <random|one|all|half>."""
    if shape == "uniform":
        pages = [rng.randint(1, 500) for _ in range(n)]
    elif shape == "max":
        pages = [500] * n
    elif shape == "ones":
        pages = [1] * n
    elif shape == "ascending":
        pages = sorted(rng.randint(1, 500) for _ in range(n))
    elif shape == "descending":
        pages = sorted((rng.randint(1, 500) for _ in range(n)), reverse=True)
    elif shape == "one-big":
        pages = [1] * n
        pages[rng.randrange(n)] = 500
    elif shape == "small-values":
        pages = [rng.randint(1, 3) for _ in range(n)]
    else:
        raise ValueError("unknown shape: %s" % shape)

    if days == "one":
        d = 1
    elif days == "all":
        d = n
    elif days == "half":
        d = max(1, n // 2)
    else:
        d = rng.randint(1, n)
    return {"pages": pages, "days": d}
