import collections


def shape(rng, n, kind="random"):
    """Child indexes (-1 for none) of a random n-node tree rooted at 0."""
    L, R = [-1] * n, [-1] * n
    for i in range(1, n):
        if kind in ("line", "left-line", "right-line"):
            p = i - 1
            side = {"left-line": 0, "right-line": 1}.get(kind, rng.randint(0, 1))
        elif kind == "full":
            p, side = (i - 1) // 2, (i - 1) % 2
        else:
            while True:
                p = rng.randrange(i)
                free = [s for s in (0, 1) if (L, R)[s][p] == -1]
                if free:
                    side = rng.choice(free)
                    break
        (L, R)[side][p] = i
    return L, R


def level(vals, L, R, root=0):
    """Level order with None for gaps, trailing Nones trimmed."""
    if root < 0 or root >= len(vals):
        return []
    out, q = [], collections.deque([root])
    while q:
        i = q.popleft()
        if i < 0:
            out.append(None)
            continue
        out.append(vals[i])
        q.append(L[i])
        q.append(R[i])
    while out and out[-1] is None:
        out.pop()
    return out


def tree_with(rng, n, kind):
    L, R = shape(rng, n, kind)
    vals = rng.sample(range(10**5 + 1), n)
    return vals, L, R


def depths(n, L, R):
    d = [0] * n
    for i in range(n):
        for c in (L[i], R[i]):
            if c >= 0:
                d[c] = d[i] + 1
    return d


def build(rng, n, kind="random", rel="any"):
    vals, L, R = tree_with(rng, n, kind)
    if rel == "same":
        i = j = rng.randrange(n)
    elif rel == "deep":
        dep = depths(n, L, R)
        order = sorted(range(n), key=lambda i: -dep[i])
        i, j = order[0], order[min(1, n - 1)]
    else:
        i, j = rng.randrange(n), rng.randrange(n)
    return {"root": level(vals, L, R), "p": vals[i], "q": vals[j]}


def small(rng):
    return build(rng, rng.randint(1, 7), rng.choice(("random", "line")), rng.choice(("any", "any", "same")))
