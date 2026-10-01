def grid01(rng, m, n, density):
    return [[1 if rng.random() < density else 0 for _ in range(n)] for _ in range(m)]


def small(rng):
    return {"board": grid01(rng, rng.randint(1, 4), rng.randint(1, 4), rng.choice((0.3, 0.5, 0.7)))}


def build(rng, m, n, density=40):
    return {"board": grid01(rng, m, n, density / 100)}
