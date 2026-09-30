def make(rng, n, frac):
    cells = [[r, c] for r in range(n) for c in range(n)]
    rng.shuffle(cells)
    return {"n": n, "holes": cells[:int(len(cells) * frac)]}
def small(rng):
    n = rng.randint(1, 6)
    return make(rng, n, rng.choice([0, 0.05, 0.1, 0.2]))
def build(rng, n, frac=0.1, shape="random"):
    if shape == "diagonal":
        return {"n": n, "holes": [[i, i] for i in range(n)]}
    if shape == "column":
        c = rng.randrange(n)
        return {"n": n, "holes": [[r, c] for r in range(n) if r != rng.randrange(n)]}
    if shape == "center":
        m = n // 2
        return {"n": n, "holes": [[r, c] for r in range(m - 1, m + 2) for c in range(m - 1, m + 2) if 0 <= r < n and 0 <= c < n]}
    return make(rng, n, frac)
