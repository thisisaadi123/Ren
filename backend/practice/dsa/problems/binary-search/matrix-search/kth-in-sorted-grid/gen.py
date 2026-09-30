def make(rng, n, step):
    g = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            base = max(g[i - 1][j] if i else -10**9, g[i][j - 1] if j else -10**9)
            g[i][j] = min(10**9, base + rng.randint(0, step))
    return {"grid": g, "k": rng.randint(1, n * n)}
def small(rng):
    return make(rng, rng.randint(1, 4), rng.choice([0, 2, 5]))
def build(rng, n, step=10**6):
    return make(rng, n, step)
