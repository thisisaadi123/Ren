from ren_gen import tree, _level_order


def comb(rng, n, pick):
    spine = (n + 1) // 2
    kids = {i: [None, None] for i in range(n)}
    nxt = spine
    for i in range(spine):
        side = rng.randint(0, 1)
        if i + 1 < spine:
            kids[i][side] = i + 1
        if nxt < n:
            kids[i][1 - side] = nxt
            nxt += 1
    return _level_order(kids, [pick() for _ in range(n)])


def shaped(rng, n, shape, pick):
    if shape == "comb":
        return comb(rng, n, pick)
    return tree(rng, n, shape=shape, values=[pick() for _ in range(n)])


def small(rng):
    n = rng.randint(1, 9)
    hi = rng.choice([1, 2, 25])
    return {"root": shaped(rng, n, rng.choice(["random", "line", "full", "comb"]), lambda: rng.randint(0, hi))}


def build(rng, n, shape="random", lo=0, hi=25):
    return {"root": shaped(rng, n, shape, lambda: rng.randint(lo, hi))}
