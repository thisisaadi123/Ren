"""Shared input builders for gen.py files. Every function takes a seeded random.Random.

    from ren_gen import ints, word, tree, graph, grid
"""
import collections
import string

LOWER = string.ascii_lowercase


def ints(rng, n, lo, hi):
    return [rng.randint(lo, hi) for _ in range(n)]


def distinct(rng, n, lo, hi):
    return rng.sample(range(lo, hi + 1), n)


def word(rng, n, alphabet=LOWER):
    return "".join(rng.choice(alphabet) for _ in range(n))


def words(rng, count, min_len, max_len, alphabet=LOWER):
    return [word(rng, rng.randint(min_len, max_len), alphabet) for _ in range(count)]


def matrix(rng, rows, cols, lo, hi):
    return [ints(rng, cols, lo, hi) for _ in range(rows)]


def grid(rng, rows, cols, cells="01", weights=None):
    """rows x cols grid of single-character strings chosen from `cells`."""
    return [[rng.choices(cells, weights)[0] for _ in range(cols)] for _ in range(rows)]


def _level_order(kids, values):
    if not values:
        return []
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


def tree(rng, n, lo=-1000, hi=1000, shape="random", values=None):
    """A binary tree with n nodes in level order (None for gaps).
    shape: random | full (complete) | line (random zigzag chain) | left-line | right-line."""
    if n == 0:
        return []
    kids = {0: [None, None]}
    for i in range(1, n):
        if shape in ("line", "left-line", "right-line"):
            p = i - 1
            side = {"left-line": 0, "right-line": 1}.get(shape, rng.randint(0, 1))
        elif shape == "full":
            p, side = (i - 1) // 2, (i - 1) % 2
        else:
            while True:
                p = rng.randrange(i)
                free = [s for s in (0, 1) if kids[p][s] is None]
                if free:
                    side = rng.choice(free)
                    break
        kids[p][side] = i
        kids[i] = [None, None]
    if values is None:
        values = [rng.randint(lo, hi) for _ in range(n)]
    return _level_order(kids, values)


def bst(rng, n, lo=-10**4, hi=10**4, order="random"):
    """A BST of n distinct keys in level order. order: random | sorted (a right chain) | balanced."""
    keys = sorted(distinct(rng, n, lo, hi))
    if order == "balanced":
        seq = []

        def mid(a, b):
            if a > b:
                return
            m = (a + b) // 2
            seq.append(keys[m])
            mid(a, m - 1)
            mid(m + 1, b)

        mid(0, n - 1)
    elif order == "sorted":
        seq = keys
    else:
        seq = keys[:]
        rng.shuffle(seq)
    if not seq:
        return []
    left, right = {}, {}
    root = seq[0]
    for k in seq[1:]:
        cur = root
        while True:
            side = left if k < cur else right
            if cur in side:
                cur = side[cur]
            else:
                side[cur] = k
                break
    idx = {k: i for i, k in enumerate(seq)}
    kids = {idx[k]: [idx[left[k]] if k in left else None, idx[right[k]] if k in right else None] for k in seq}
    return _level_order(kids, seq)


def graph(rng, n, m, directed=False, weights=None, connected=False, allow_self=False, simple=True):
    """Edges [u, v] or [u, v, w] over nodes 0..n-1. weights=(lo, hi) adds a weight.
    connected=True starts from a random spanning tree (needs m >= n - 1)."""
    edges, seen = [], set()

    def add(u, v):
        key = (u, v) if directed else (min(u, v), max(u, v))
        if simple and key in seen:
            return False
        seen.add(key)
        e = [u, v]
        if weights:
            e.append(rng.randint(*weights))
        edges.append(e)
        return True

    if connected and n > 1:
        order = list(range(n))
        rng.shuffle(order)
        for i in range(1, n):
            u, v = order[rng.randrange(i)], order[i]
            add(u, v) if rng.random() < 0.5 or not directed else add(v, u)
    cap = n * (n - 1) if directed else n * (n - 1) // 2
    if allow_self:
        cap += n
    tries = 0
    while len(edges) < min(m, cap if simple else m) and tries < 50 * (m + 1):
        tries += 1
        u, v = rng.randrange(n), rng.randrange(n)
        if u == v and not allow_self:
            continue
        add(u, v)
    rng.shuffle(edges)
    return edges


def dag(rng, n, m):
    """Directed acyclic edges: every edge goes from an earlier to a later node in a hidden order."""
    order = list(range(n))
    rng.shuffle(order)
    rank = {v: i for i, v in enumerate(order)}
    edges = set()
    tries = 0
    while len(edges) < min(m, n * (n - 1) // 2) and tries < 50 * (m + 1):
        tries += 1
        u, v = rng.sample(range(n), 2) if n > 1 else (0, 0)
        if u == v:
            continue
        if rank[u] > rank[v]:
            u, v = v, u
        edges.add((u, v))
    out = [list(e) for e in edges]
    rng.shuffle(out)
    return out
