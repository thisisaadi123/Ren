import collections
from ren_gen import tree


def width(root):
    it = iter(root[1:])
    level, best = [0], 1
    while level:
        best = max(best, level[-1] - level[0] + 1)
        nxt = []
        for p in level:
            p -= level[0]
            for side in (0, 1):
                if next(it, None) is not None:
                    nxt.append(2 * p + side)
        level = nxt
    return best


def level_order(kids, n, rng):
    vals = [rng.randint(-1000, 1000) for _ in range(n)]
    out, q = [], collections.deque([0])
    while q:
        i = q.popleft()
        if i is None:
            out.append(None)
            continue
        out.append(vals[i])
        q.extend(kids[i])
    while out and out[-1] is None:
        out.pop()
    return out


def vee(rng, n, arm):
    # two arms going down the far left and far right edges, then a long chain under the left arm
    kids = {0: [None, None]}
    nxt = 1
    for side in (0, 1):
        cur = 0
        for _ in range(arm):
            if nxt >= n:
                break
            kids[cur][side] = nxt
            kids[nxt] = [None, None]
            cur, nxt = nxt, nxt + 1
    cur = kids[0][0] or 0
    while kids[cur][0] is not None:
        cur = kids[cur][0]
    while nxt < n:
        kids[cur][rng.randint(0, 1)] = nxt
        kids[nxt] = [None, None]
        cur, nxt = nxt, nxt + 1
    return level_order(kids, n, rng)


def small(rng):
    n = rng.randint(1, 9)
    if rng.random() < 0.2:
        return {"root": vee(rng, n, rng.randint(1, 4))}
    return {"root": tree(rng, n, -9, 9, shape=rng.choice(["random", "random", "line", "full"]))}


def build(rng, n, shape="random", arm=59):
    if shape == "vee":
        return {"root": vee(rng, n, arm)}
    while True:
        root = tree(rng, n, -1000, 1000, shape=shape)
        if width(root) <= 10**18:
            return {"root": root}
