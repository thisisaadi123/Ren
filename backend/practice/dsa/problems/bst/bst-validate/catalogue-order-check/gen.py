import collections


def parse(root):
    """Level order -> (vals, L, R): node k is the k-th non-null entry; -1 means no child."""
    vals, L, R = [], [], []
    if not root:
        return vals, L, R
    vals.append(root[0]); L.append(-1); R.append(-1)
    q = collections.deque([0])
    i = 1
    while q and i < len(root):
        p = q.popleft()
        for side in (L, R):
            if i < len(root) and root[i] is not None:
                vals.append(root[i]); L.append(-1); R.append(-1)
                side[p] = len(vals) - 1
                q.append(len(vals) - 1)
            i += 1
    return vals, L, R


def serialize(vals, L, R, r=0):
    if r == -1 or not vals:
        return []
    out, q = [], collections.deque([r])
    while q:
        x = q.popleft()
        if x == -1:
            out.append(None)
            continue
        out.append(vals[x])
        q.append(L[x]); q.append(R[x])
    while out and out[-1] is None:
        out.pop()
    return out


def inorder(L, R, r=0):
    out, st, x = [], [], r if L else -1
    while st or x != -1:
        while x != -1:
            st.append(x); x = L[x]
        x = st.pop(); out.append(x); x = R[x]
    return out


def height(L, R, r=0):
    if not L or r == -1:
        return 0
    h, level = 0, [r]
    while level:
        h += 1
        level = [c for x in level for c in (L[x], R[x]) if c != -1]
    return h


def chain_bst(keys, left=False):
    """A search-tree chain from sorted keys: a right chain (ascending) or a left chain."""
    keys = sorted(keys)
    if not keys:
        return []
    if not left:
        out = [keys[0]]
        for k in keys[1:]:
            out += [None, k]
        return out
    out = [keys[-1]]
    for k in reversed(keys[:-1]):
        out += [k, None]
    while out and out[-1] is None:
        out.pop()
    return out


def fast_bst(rng, n, lo, hi, order="random"):
    """ren_gen.bst, but sorted order (a chain) is built in O(n) instead of by n insertions."""
    from ren_gen import bst as _bst, distinct as _distinct
    if order in ("sorted", "left-chain"):
        return chain_bst(_distinct(rng, n, lo, hi), left=(order == "left-chain"))
    return _bst(rng, n, lo, hi, order)

from ren_gen import bst, tree as rtree

LO, HI = -2**31, 2**31 - 1


def bounds(vals, L, R):
    """For each node: (low, low_from, high, high_from) where *_from is the ancestor giving the bound."""
    out = [None] * len(vals)
    out[0] = (None, -1, None, -1)
    for x in range(len(vals)):
        lo, lf, hi, hf = out[x]
        if L[x] != -1:
            out[L[x]] = (lo, lf, vals[x], x)
        if R[x] != -1:
            out[R[x]] = (vals[x], x, hi, hf)
    return out


def parent_of(L, R):
    par = [-1] * len(L)
    for x in range(len(L)):
        for c in (L[x], R[x]):
            if c != -1:
                par[c] = x
    return par


def make(rng, n, kind, lo, hi, order=None):
    order = order or rng.choice(["random", "random", "sorted", "balanced"])
    if kind == "random":
        return rtree(rng, n, lo, hi, shape=rng.choice(["random", "line", "full"]))
    root = fast_bst(rng, n, lo, hi, order)
    if kind == "valid" or n < 2:
        return root
    vals, L, R = parse(root)
    if kind == "swap":
        i, j = rng.sample(range(n), 2)
        vals[i], vals[j] = vals[j], vals[i]
    elif kind == "dup":
        par = parent_of(L, R)
        x = rng.randrange(1, n)
        anc = []
        p = par[x]
        while p != -1:
            anc.append(p)
            p = par[p]
        vals[x] = vals[rng.choice(anc)]
    elif kind == "far":
        # Break the rule against a far ancestor while every parent-child pair still looks right.
        b = bounds(vals, L, R)
        par = parent_of(L, R)
        cands = []
        for x in range(1, n):
            lo_, lf, hi_, hf = b[x]
            p = par[x]
            if hf != -1 and hf != p and hi_ < HI - 2:
                cands.append((x, "hi"))
            if lf != -1 and lf != p and lo_ > LO + 2:
                cands.append((x, "lo"))
        leaves = [c for c in cands if L[c[0]] == -1 and R[c[0]] == -1]
        pool = leaves or cands
        if pool:
            x, side = rng.choice(pool)
            lo_, lf, hi_, hf = b[x]
            vals[x] = hi_ + rng.randint(0, 2) if side == "hi" else lo_ - rng.randint(0, 2)
        else:
            i, j = rng.sample(range(n), 2)
            vals[i], vals[j] = vals[j], vals[i]
    return serialize(vals, L, R)


def small(rng):
    n = rng.randint(1, 7)
    kind = rng.choice(["valid", "valid", "swap", "far", "far", "dup", "random"])
    return {"root": make(rng, n, kind, -20, 20)}


def build(rng, n, kind="valid", order=None, wide=False):
    lo, hi = (LO, HI) if wide else (-10**6, 10**6)
    return {"root": make(rng, n, kind, lo, hi, order)}
