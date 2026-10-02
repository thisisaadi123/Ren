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


def build(rng, n, rights=50):
    # A left spine with some right leaves hanging off it.
    vals = rng.sample(range(1, 10**4 + 1), n) if n else []
    L, R = [-1] * n, [-1] * n
    spine = [0] if n else []
    i = 1
    while i < n:
        p = spine[-1]
        L[p] = i
        spine.append(i)
        i += 1
        if i < n and rng.randrange(100) < rights:
            R[p] = i
            i += 1
    return {"root": level(vals, L, R)}


def small(rng):
    return build(rng, rng.randint(0, 7), rng.choice((0, 50, 100)))
