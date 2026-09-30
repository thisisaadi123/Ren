def small(rng):
    n = rng.randint(1, 6)
    vals = rng.sample(range(-10, 11), rng.randint(1, 3))
    return {"beads": [rng.choice(vals) for _ in range(n)]}
def build(rng, n, k=3, shape="random"):
    if shape == "distinct":
        return {"beads": rng.sample(range(-10, 11), n)}
    vals = rng.sample(range(-10, 11), k)
    b = [rng.choice(vals) for _ in range(n)]
    return {"beads": b}
