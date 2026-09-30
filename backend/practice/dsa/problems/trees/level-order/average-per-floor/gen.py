from ren_gen import tree


def small(rng):
    n = rng.randint(1, 8)
    return {"root": tree(rng, n, -9, 9, shape=rng.choice(["random", "random", "line", "full"]))}


def build(rng, n, shape="random", lo=-10**9, hi=10**9):
    return {"root": tree(rng, n, lo, hi, shape=shape)}
