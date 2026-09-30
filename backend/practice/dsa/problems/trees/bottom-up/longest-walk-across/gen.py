from ren_gen import tree, _level_order


def lollipop(rng, n, pick):
    # a long chain hanging off the root's left child, with a bushy full tree on the right:
    # the longest walk does not pass through the root.
    kids = {i: [None, None] for i in range(n)}
    chain = max(1, n // 3) if n > 1 else 0
    # root 0, left child 1 starts a zigzag chain, right child starts a small full tree
    for i in range(1, chain):
        kids[i][rng.randint(0, 1)] = i + 1
    if n > 1:
        kids[0][0] = 1
    # second long chain from node 1's free side so the best walk bends at node 1
    free = [s for s in (0, 1) if kids[1][s] is None] if n > 1 else []
    nxt = chain + 1
    if free and nxt < n:
        side = free[0]
        cur = 1
        for _ in range(n // 3):
            if nxt >= n:
                break
            kids[cur][side] = nxt
            cur, nxt, side = nxt, nxt + 1, rng.randint(0, 1)
    # the rest: a full tree under the root's right child
    rest = list(range(nxt, n))
    if rest:
        kids[0][1] = rest[0]
        for j in range(1, len(rest)):
            p = rest[(j - 1) // 2]
            kids[p][(j - 1) % 2] = rest[j]
    return _level_order(kids, [pick() for _ in range(n)])


def shaped(rng, n, shape, pick):
    if shape == "lollipop":
        return lollipop(rng, n, pick)
    return tree(rng, n, shape=shape, values=[pick() for _ in range(n)])


def small(rng):
    n = rng.randint(1, 9)
    return {"root": shaped(rng, n, rng.choice(["random", "line", "full", "lollipop"]), lambda: rng.randint(-9, 9))}


def build(rng, n, shape="random"):
    return {"root": shaped(rng, n, shape, lambda: rng.randint(-1000, 1000))}
