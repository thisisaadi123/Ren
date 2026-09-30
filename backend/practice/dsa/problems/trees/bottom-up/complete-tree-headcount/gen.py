def small(rng):
    n = rng.randint(0, 16)
    return {"root": [rng.randint(-9, 9) for _ in range(n)]}


def build(rng, n=None, upto=None):
    if n is None:
        n = rng.randint(1, upto)
    return {"root": [rng.randint(-1000, 1000) for _ in range(n)]}
