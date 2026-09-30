def small(rng):
    guide = rng.sample(range(0, 8), rng.randint(1, 4))
    return {"items": [rng.randint(0, 9) for _ in range(rng.randint(1, 8))], "guide": guide}
def build(rng, n, g=100, hi=1000):
    guide = rng.sample(range(0, hi + 1), min(g, hi + 1))
    return {"items": [rng.randint(0, hi) for _ in range(n)], "guide": guide}
