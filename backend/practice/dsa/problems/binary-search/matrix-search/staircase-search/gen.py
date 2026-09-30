def make(rng, m, n, step, hit):
    g = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            base = max(g[i - 1][j] if i else -10**9 // 2, g[i][j - 1] if j else -10**9 // 2)
            g[i][j] = min(10**9, base + rng.randint(0, step))
    t = rng.choice(rng.choice(g)) if hit else rng.randint(g[0][0] - 2, g[-1][-1] + 2)
    return {"grid": g, "target": t}
def small(rng):
    return make(rng, rng.randint(1, 4), rng.randint(1, 4), 3, rng.random() < 0.5)
def build(rng, m, n, step=1000, hit=1):
    return make(rng, m, n, step, bool(hit))
