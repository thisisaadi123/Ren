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


def mirror_tree(rng, half, kind, hi, breaks=0):
    """A symmetric tree from a random half: root, the half on the left, its mirror on the right."""
    L, R = shape(rng, half, kind)
    vals = [rng.randint(-hi, hi) for _ in range(half)]
    n = 2 * half + 1
    V, LL, RR = [0] * n, [-1] * n, [-1] * n
    V[0] = rng.randint(-hi, hi)
    if half:
        LL[0], RR[0] = 1, 1 + half
    for i in range(half):
        a, b = 1 + i, 1 + half + i
        V[a] = V[b] = vals[i]
        LL[a] = 1 + L[i] if L[i] >= 0 else -1
        RR[a] = 1 + R[i] if R[i] >= 0 else -1
        LL[b] = 1 + half + R[i] if R[i] >= 0 else -1
        RR[b] = 1 + half + L[i] if L[i] >= 0 else -1
    for _ in range(breaks):
        j = rng.randrange(1, n) if n > 1 else 0
        V[j] = V[j] + 1 if V[j] < hi else V[j] - 1
    return level(V, LL, RR)


def build(rng, half, kind="random", hi=100, breaks=0, shape_kind=""):
    if shape_kind == "random-tree":
        n = 2 * half + 1
        L, R = shape(rng, n, kind)
        return {"root": level([rng.randint(-hi, hi) for _ in range(n)], L, R)}
    return {"root": mirror_tree(rng, half, kind, hi, breaks)}


def small(rng):
    r = rng.random()
    if r < 0.4:
        return build(rng, rng.randint(0, 3), "random", 2)
    if r < 0.7:
        return build(rng, rng.randint(1, 3), "random", 2, 1)
    return build(rng, rng.randint(0, 2), "random", 1, 0, "random-tree")
