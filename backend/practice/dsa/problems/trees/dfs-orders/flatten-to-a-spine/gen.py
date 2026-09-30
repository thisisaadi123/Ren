from ren_gen import tree


def small(rng):
    n = rng.randint(0, 8)
    return {"root": tree(rng, n, -9, 9, shape=rng.choice(["random", "random", "line", "full"]))}


def build(rng, n, shape="random", lo=-1000, hi=1000):
    return {"root": tree(rng, n, lo, hi, shape=shape)}
