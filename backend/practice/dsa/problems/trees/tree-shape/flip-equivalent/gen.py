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


def build(rng, n, flips=50, change="none", kind="random"):
    L, R = shape(rng, n, kind)
    vals = rng.sample(range(10**5 + 1), n)
    a = level(vals, L, R)
    L2, R2 = L[:], R[:]
    for i in range(n):
        if rng.randrange(100) < flips:
            L2[i], R2[i] = R2[i], L2[i]
    v2 = vals[:]
    if change == "swap-values" and n >= 2:
        i, j = rng.sample(range(n), 2)
        v2[i], v2[j] = v2[j], v2[i]
    elif change == "move" and n >= 3:
        # Move one leaf to a different free spot.
        leaves = [i for i in range(1, n) if L2[i] < 0 and R2[i] < 0]
        x = rng.choice(leaves)
        for p in range(n):
            if L2[p] == x:
                L2[p] = -1
            if R2[p] == x:
                R2[p] = -1
        spots = [(p, s) for p in range(n) if p != x for s in (0, 1) if (L2, R2)[s][p] < 0]
        p, s = rng.choice(spots)
        (L2, R2)[s][p] = x
    return {"a": a, "b": level(v2, L2, R2)}


def small(rng):
    return build(rng, rng.randint(0, 6), 50, rng.choice(("none", "none", "swap-values", "move")))
