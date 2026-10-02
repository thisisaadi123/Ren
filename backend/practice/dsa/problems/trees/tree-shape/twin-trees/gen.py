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


def build(rng, n, change="none", kind="random", hi=10**4):
    L, R = shape(rng, n, kind)
    vals = [rng.randint(-hi, hi) for _ in range(n)]
    a = level(vals, L, R)
    if change == "value" and n:
        v2 = vals[:]
        i = rng.randrange(n)
        v2[i] = v2[i] + 1 if v2[i] < hi else v2[i] - 1
        return {"a": a, "b": level(v2, L, R)}
    if change == "shape" and n:
        # Mirror one node's children, which changes the shape unless it's symmetric.
        L2, R2 = L[:], R[:]
        i = rng.randrange(n)
        L2[i], R2[i] = R2[i], L2[i]
        return {"a": a, "b": level(vals, L2, R2)}
    if change == "other":
        L2, R2 = shape(rng, n, kind)
        return {"a": a, "b": level(vals, L2, R2)}
    return {"a": a, "b": a}


def small(rng):
    return build(rng, rng.randint(0, 5), rng.choice(("none", "value", "shape", "other")), "random", rng.choice((1, 3)))
