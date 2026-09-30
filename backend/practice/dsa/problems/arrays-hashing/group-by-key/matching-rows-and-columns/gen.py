from ren_gen import matrix
def sym(rng, n, hi):
    g = matrix(rng, n, n, 1, hi)
    for i in range(n):
        for j in range(i):
            if rng.random() < 0.7:
                g[i][j] = g[j][i]
    return g
def small(rng):
    n = rng.randint(1, 4)
    return {"grid": sym(rng, n, 2) if rng.random() < 0.5 else matrix(rng, n, n, 1, 2)}
def build(rng, n, hi=3, shape="sym"):
    return {"grid": sym(rng, n, hi) if shape == "sym" else matrix(rng, n, n, 1, hi)}
