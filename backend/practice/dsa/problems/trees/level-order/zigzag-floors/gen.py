from ren_gen import tree


def small(rng):
    n = rng.randint(0, 9)
    return {"root": tree(rng, n, -9, 9, shape=rng.choice(["random", "random", "line", "full"]))}


def build(rng, n, shape="random"):
    return {"root": tree(rng, n, -1000, 1000, shape=shape)}
