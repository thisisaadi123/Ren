from ren_gen import tree


def small(rng):
    n = rng.randint(1, 9)
    return {"root": tree(rng, n, 1, 9, shape=rng.choice(["random", "random", "line", "full"]))}


def build(rng, n, shape="random", lo=1, hi=10**4):
    return {"root": tree(rng, n, lo, hi, shape=shape)}
