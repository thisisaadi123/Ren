from ren_gen import ints


def build(rng, n, k=0, lo=-10**4, hi=10**4):
    return {"stones": ints(rng, n, lo, hi), "k": k or rng.randint(1, n)}


def small(rng):
    n = rng.randint(1, 8)
    return build(rng, n, rng.randint(1, n + 1), -5, 5)
