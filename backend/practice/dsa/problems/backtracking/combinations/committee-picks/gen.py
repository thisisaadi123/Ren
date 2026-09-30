def small(rng):
    n = rng.randint(1, 8)
    return {"n": n, "k": rng.randint(1, n)}
def build(rng, n, k=0):
    return {"n": n, "k": k if k else rng.randint(1, n)}
