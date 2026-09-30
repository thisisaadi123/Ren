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



def mirror_comb(rng, n, hi):
    # spine digits form a long palindrome; each spine node's hanging leaf repeats the spine's first digit,
    # so many trails come close to mirroring and some do.
    spine = (n + 1) // 2
    half = [rng.randint(1, hi) for _ in range((spine + 1) // 2)]
    seq = half + half[::-1][spine % 2:]
    seq = seq[:spine]
    kids = {i: [None, None] for i in range(n)}
    vals = seq + [seq[0]] * (n - spine)
    nxt = spine
    for i in range(spine):
        if i + 1 < spine:
            kids[i][0] = i + 1
        if nxt < n:
            kids[i][1] = nxt
            nxt += 1
    return _level_order(kids, vals)


def small(rng):
    n = rng.randint(1, 9)
    hi = rng.choice([1, 2, 2, 3, 9])
    if rng.random() < 0.2:
        return {"root": mirror_comb(rng, n, hi)}
    return {"root": shaped(rng, n, rng.choice(["random", "line", "full", "comb"]), lambda: rng.randint(1, hi))}


def build(rng, n, shape="random", hi=9):
    if shape == "mirror-comb":
        return {"root": mirror_comb(rng, n, hi)}
    return {"root": shaped(rng, n, shape, lambda: rng.randint(1, hi))}
