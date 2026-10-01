from ren_gen import distinct


def build(rng, n, hi=10**9):
    return {"cards": distinct(rng, n, 1, hi)}


def small(rng):
    return build(rng, rng.randint(1, 6), rng.choice((10, 100)))
