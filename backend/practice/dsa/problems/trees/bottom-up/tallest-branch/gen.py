import collections


def level_order(n, rng, shape):
    """A random tree with n nodes, returned in level order with None gaps."""
    if n == 0:
        return []
    # parent links: node i attaches to a random earlier node with a free side
    kids = {0: [None, None]}
    for i in range(1, n):
        if shape == "line":
            p, side = i - 1, 0 if rng.random() < 0.5 else 1
        elif shape == "left-line":
            p, side = i - 1, 0
        else:
            while True:
                p = rng.randrange(i) if shape == "random" else (i - 1) // 2
                free = [s for s in (0, 1) if kids[p][s] is None]
                if free:
                    side = rng.choice(free) if shape == "random" else free[0]
                    break
        kids[p][side] = i
        kids[i] = [None, None]
    values = [rng.randint(-1000, 1000) for _ in range(n)]
    out, queue = [], collections.deque([0])
    while queue:
        i = queue.popleft()
        if i is None:
            out.append(None)
            continue
        out.append(values[i])
        queue.extend(kids[i])
    while out and out[-1] is None:
        out.pop()
    return out


def small(rng):
    return {"root": level_order(rng.randint(0, 9), rng, rng.choice(["random", "line", "full"]))}


def build(rng, n, shape="random"):
    return {"root": level_order(n, rng, shape)}
