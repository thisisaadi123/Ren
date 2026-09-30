def small(rng):
    return {"pieces": [rng.choice([0, 1, 3, 9, 10, 30, 34, 5, 99, 90, 909]) for _ in range(rng.randint(1, 6))]}
def build(rng, n, hi=10**9, zeros=False):
    if zeros:
        return {"pieces": [0] * n}
    return {"pieces": [rng.randint(0, hi) for _ in range(n)]}
