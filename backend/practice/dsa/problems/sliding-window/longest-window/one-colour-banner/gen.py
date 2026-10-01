from ren_gen import word

UP = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def build(rng, n, k=-1, alpha=4):
    return {"s": word(rng, n, UP[:alpha]), "k": k if k >= 0 else rng.randint(0, n)}


def small(rng):
    n = rng.randint(1, 8)
    return build(rng, n, rng.randint(0, min(n, 3)), rng.choice((2, 3, 26)))
