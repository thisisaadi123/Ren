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
    n = rng.randint(0, 8)
    root = shaped(rng, n, rng.choice(["random", "line", "full", "comb"]), lambda: rng.randint(-5, 5))
    return {"root": root, "target": rng.randint(-8, 8)}


def build(rng, n, shape="random", lo=-1000, hi=1000, hit="maybe"):
    root = shaped(rng, n, shape, lambda: rng.randint(lo, hi))
    # pick a real trail total (hit), a total just off one (miss), or anything
    from ren_gen import tree as _t
    vals = root
    # recompute trail totals from the level order
    import collections
    totals, q, it = [], collections.deque([(0, vals[0])]) if vals else collections.deque(), iter(vals[1:])
    while q:
        _, s = q.popleft()
        kids = [next(it, None), next(it, None)]
        real = [k for k in kids if k is not None]
        if not real:
            totals.append(s)
        for k in real:
            q.append((0, s + k))
    if hit == "yes" and totals:
        target = rng.choice(totals)
    elif hit == "no":
        have = set(totals)
        target = max(totals) + 1 if totals else 0
        while target in have:
            target += 1
    else:
        target = rng.randint(-3000, 3000)
    return {"root": root, "target": target}
