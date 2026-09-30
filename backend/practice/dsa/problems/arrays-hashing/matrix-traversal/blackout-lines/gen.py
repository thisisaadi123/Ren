def make(rng, m, n, p):
    return [[0 if rng.random() < p else rng.randint(1, 9) * rng.choice([1, -1]) for _ in range(n)] for _ in range(m)]
def small(rng):
    return {"grid": make(rng, rng.randint(1, 4), rng.randint(1, 4), rng.choice([0.0, 0.15, 0.4]))}
def build(rng, m, n, p=0.01):
    return {"grid": make(rng, m, n, p)}
