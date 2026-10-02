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


def encode(vals, L, R):
    out, stack = [], [0]
    while stack:
        item = stack.pop()
        if isinstance(item, str):
            out.append(item)
            continue
        out.append(str(vals[item]))
        if R[item] >= 0:
            stack += [")", R[item], "("]
        if L[item] >= 0:
            stack += [")", L[item], "("]
        elif R[item] >= 0:
            stack.append("()")
    return "".join(out)


def build(rng, n, kind="random", hi=1000):
    vals, L, R = rand_tree(rng, n, kind, -hi, hi)
    s = encode(vals, L, R)
    while len(s) > 30_000 and n > 1:
        n = n * 3 // 4
        vals, L, R = rand_tree(rng, n, kind, -hi, hi)
        s = encode(vals, L, R)
    return {"s": s}


def small(rng):
    return build(rng, rng.randint(1, 7), rng.choice(("random", "line", "right-line")), rng.choice((9, 1000)))
