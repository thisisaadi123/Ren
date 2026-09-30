def small(rng):
    n = rng.randint(1, 9)
    k = rng.randint(1, n)
    return {"balls": [rng.randint(1, k) for _ in range(n)], "k": k}
def build(rng, n, k=5):
    k = min(k, n)
    return {"balls": [rng.randint(1, k) for _ in range(n)], "k": k}
