def small(rng):
    r, c = rng.randint(1, 6), rng.randint(1, 6)
    return {"rows": r, "cols": c, "k": rng.randint(1, r * c)}
def build(rng, rows, cols, where="random"):
    k = {"first": 1, "last": rows * cols}.get(where) or rng.randint(1, rows * cols)
    return {"rows": rows, "cols": cols, "k": k}
