def small(rng):
    n = rng.randint(1, 4)
    return {"stamps": rng.sample(range(2, 12), n), "target": rng.randint(1, 16)}
def build(rng, n, target=0, lo=2, hi=40):
    n = min(n, hi - lo + 1)
    return {"stamps": rng.sample(range(lo, hi + 1), n), "target": target if target else rng.randint(1, 40)}
