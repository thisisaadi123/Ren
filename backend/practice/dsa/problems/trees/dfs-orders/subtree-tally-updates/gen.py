from ren_gen import tree, distinct


def make(rng, n, q, shape, xmax, top=False):
    vals = distinct(rng, n, 1, 10**6 if n > 50 else 60)
    root = tree(rng, n, shape=shape, values=vals)
    order = [v for v in root if v is not None]
    ops = []
    for _ in range(q):
        if rng.random() < 0.5:
            v = order[n - 1 - rng.randrange(min(5, n))] if top else rng.choice(order)
            ops.append([1, v, rng.randint(1, xmax)])
        else:
            v = order[rng.randrange(min(3, n))] if top else rng.choice(order)
            ops.append([2, v])
    return {"root": root, "ops": ops}


def small(rng):
    return make(rng, rng.randint(1, 6), rng.randint(1, 5), rng.choice(["random", "line", "full"]), 9)


def build(rng, n, q, shape="random", xmax=10**9, top=False):
    return make(rng, n, q, shape, xmax, top)
