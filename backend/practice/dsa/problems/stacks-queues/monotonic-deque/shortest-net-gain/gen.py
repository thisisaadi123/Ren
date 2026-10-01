from ren_gen import ints


def build(rng, n, lo=-10**5, hi=10**5, target=0):
    a = ints(rng, n, lo, hi)
    return {"changes": a, "target": target or rng.randint(1, max(1, hi * 3))}


def small(rng):
    return build(rng, rng.randint(1, 8), -5, 5, rng.randint(1, 12))
