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


def sub_level(vals, L, R, i):
    return level(vals, L, R, i)


def build(rng, n, hi=3, mode="inside", kind="random"):
    L, R = shape(rng, n, kind)
    vals = [rng.randint(-hi, hi) for _ in range(n)]
    root = level(vals, L, R)
    i = rng.randrange(n)
    branch = sub_level(vals, L, R, i)
    if mode == "trim" and len(branch) > 1:
        # Drop the last node of the subtree, so it matches only the top part.
        branch = branch[:-1]
        while branch and branch[-1] is None:
            branch.pop()
    elif mode == "change":
        branch = [v if v is None or k else v + 1 for k, v in enumerate(branch)]
    elif mode == "random":
        m = rng.randint(1, max(1, min(1000, n // 3)))
        L2, R2 = shape(rng, m, "random")
        branch = level([rng.randint(-hi, hi) for _ in range(m)], L2, R2)
    return {"root": root, "branch": branch[:1000] if len(branch) <= 1000 else level([vals[i]], [-1], [-1])}


def small(rng):
    return build(rng, rng.randint(1, 7), rng.choice((0, 1)), rng.choice(("inside", "trim", "change", "random")))
