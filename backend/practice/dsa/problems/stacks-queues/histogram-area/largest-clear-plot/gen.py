def grid(rng, R, C, p):
    return [["1" if rng.random() < p else "0" for _ in range(C)] for _ in range(R)]
def small(rng):
    R, C = rng.randint(1, 4), rng.randint(1, 4)
    return {"land": grid(rng, R, C, rng.choice([0.5, 0.7, 0.9]))}
def build(rng, rows, cols, p=0.7, shape="random"):
    rows, cols, p = int(rows), int(cols), float(p)
    if shape == "planted":
        g = grid(rng, rows, cols, p)
        r1, c1 = rng.randrange(rows), rng.randrange(cols)
        r2, c2 = rng.randint(r1, rows - 1), rng.randint(c1, cols - 1)
        for r in range(r1, r2 + 1):
            for c in range(c1, c2 + 1):
                g[r][c] = "1"
        return {"land": g}
    if shape == "stripes":
        g = [["1"] * cols for _ in range(rows)]
        for r in range(rows):
            g[r][rng.randrange(cols)] = "0"
        return {"land": g}
    if shape == "staircase":
        return {"land": [["1" if c <= r * cols // rows else "0" for c in range(cols)] for r in range(rows)]}
    return {"land": grid(rng, rows, cols, p)}
