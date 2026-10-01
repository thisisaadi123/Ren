from ren_gen import matrix


def small(rng):
    hi = rng.choice((3, 255))
    return {"image": matrix(rng, rng.randint(1, 4), rng.randint(1, 4), 0, hi)}


def build(rng, m, n, hi=255):
    return {"image": matrix(rng, m, n, 0, hi)}
