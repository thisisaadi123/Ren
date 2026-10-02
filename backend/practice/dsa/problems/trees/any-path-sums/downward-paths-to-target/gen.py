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


def rand_tree(rng, n, kind, lo, hi, distinct=False):
    L, R = shape(rng, n, kind)
    vals = rng.sample(range(lo, hi + 1), n) if distinct else [rng.randint(lo, hi) for _ in range(n)]
    return vals, L, R


def build(rng, n, kind="random", lo=-10, hi=10, target=None):
    vals, L, R = rand_tree(rng, n, kind, lo, hi)
    if target is None:
        # Aim at a sum that some downward path actually has, most of the time.
        i = rng.randrange(n)
        s, cur, parent = 0, i, {c: p for p in range(n) for c in (L[p], R[p]) if c >= 0}
        for _ in range(rng.randint(1, 6)):
            s += vals[cur]
            if cur not in parent:
                break
            cur = parent[cur]
        target = s if rng.random() < 0.8 else rng.randint(lo * 3, hi * 3)
    return {"root": level(vals, L, R), "target": target}


def small(rng):
    return build(rng, rng.randint(1, 8), rng.choice(("random", "line")), -3, 3)
