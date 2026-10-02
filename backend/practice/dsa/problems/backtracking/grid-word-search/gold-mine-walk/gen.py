def build(rng, m, n, cells=10, hi=100):
    g = [[0] * n for _ in range(m)]
    spots = rng.sample([(r, c) for r in range(m) for c in range(n)], min(cells, m * n, 20))
    for r, c in spots:
        g[r][c] = rng.randint(1, hi)
    return {"mine": g}


def small(rng):
    m, n = rng.randint(1, 3), rng.randint(1, 3)
    return build(rng, m, n, rng.randint(0, m * n), 9)
