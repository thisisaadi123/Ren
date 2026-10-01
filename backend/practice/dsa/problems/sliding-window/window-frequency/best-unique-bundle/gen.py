from ren_gen import ints


def build(rng, n, k=0, hi=10**5):
    return {"prices": ints(rng, n, 1, hi), "k": min(k or rng.randint(1, n), n)}


def small(rng):
    n = rng.randint(1, 8)
    return build(rng, n, rng.randint(1, n), rng.choice((3, 6, 100)))
