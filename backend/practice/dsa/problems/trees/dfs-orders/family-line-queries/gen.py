from ren_gen import tree, distinct


def make(rng, n, q, shape, deep=False):
    vals = distinct(rng, n, 1, 10**6 if n > 50 else 60)
    root = tree(rng, n, shape=shape, values=vals)
    order = [v for v in root if v is not None]
    queries = []
    for _ in range(q):
        if deep and rng.random() < 0.9:
            # the top few against the bottom few: long walks for a naive parent climb
            a = order[rng.randrange(min(5, n))]
            b = order[n - 1 - rng.randrange(min(5, n))]
        else:
            a, b = rng.choice(order), rng.choice(order)
            if rng.random() < 0.1:
                b = a
        queries.append([a, b])
    return {"root": root, "queries": queries}


def small(rng):
    n = rng.randint(1, 7)
    return make(rng, n, rng.randint(1, 4), rng.choice(["random", "line", "full"]))


def build(rng, n, q, shape="random", deep=False):
    return make(rng, n, q, shape, deep)
