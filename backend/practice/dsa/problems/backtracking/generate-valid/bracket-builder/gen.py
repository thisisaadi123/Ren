def build(rng, lo=1, hi=10):
    return {"n": rng.randint(lo, hi)}


def small(rng):
    return {"n": rng.randint(1, 6)}
