from ren_gen import bst


def build(rng, n, order="random"):
    return {"root": bst(rng, n, 0, 10**4, order=order)}


def small(rng):
    return build(rng, rng.randint(1, 8), rng.choice(("random", "balanced", "sorted")))
