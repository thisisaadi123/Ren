def build(rng, n=10, kids=3, hi=100):
    n = max(2, n)
    return {"bags": [rng.randint(1, hi) for _ in range(n)], "kids": max(2, min(kids, n))}


def small(rng):
    n = rng.randint(2, 6)
    return build(rng, n, rng.randint(2, n), 10)
