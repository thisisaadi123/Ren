def build(rng, m, n, walls=20):
    g = [[1 if rng.randrange(100) < walls else 0 for _ in range(n)] for _ in range(m)]
    g[0][0] = g[m - 1][n - 1] = 0
    return {"maze": g}


def small(rng):
    return build(rng, rng.randint(1, 3), rng.randint(1, 3), rng.choice((0, 30)))
