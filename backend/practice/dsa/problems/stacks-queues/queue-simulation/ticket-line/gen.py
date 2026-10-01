from ren_gen import ints


def build(rng, n, hi=10**5, k=-1):
    return {"wants": ints(rng, n, 1, hi), "k": k if 0 <= k < n else rng.randrange(n)}


def small(rng):
    return build(rng, rng.randint(1, 6), rng.choice((2, 5)))
