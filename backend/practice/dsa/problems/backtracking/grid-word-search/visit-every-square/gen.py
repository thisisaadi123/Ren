def build(rng, m, n, walls=15):
    cells = [(r, c) for r in range(m) for c in range(n)]
    g = [[-1 if rng.randrange(100) < walls else 0 for _ in range(n)] for _ in range(m)]
    a, b = rng.sample(cells, 2)
    g[a[0]][a[1]] = 1
    g[b[0]][b[1]] = 2
    return {"floor": g}


def small(rng):
    m = rng.randint(1, 3)
    n = rng.randint(2 if m == 1 else 1, 3)
    return build(rng, m, n, rng.choice((0, 20)))
