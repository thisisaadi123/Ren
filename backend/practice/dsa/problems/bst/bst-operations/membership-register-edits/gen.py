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

def make_ops(rng, keys, m, lo, hi, mix):
    keys = set(keys)
    ops = []
    for _ in range(m):
        r = rng.random()
        if mix == "delete-heavy":
            kind = 0 if r < 0.7 else 1
        elif mix == "insert-heavy":
            kind = 1 if r < 0.8 else 0
        else:
            kind = 1 if r < 0.5 else 0
        if kind == 0 and keys and rng.random() < 0.85:
            k = rng.choice(sorted(keys))
        else:
            k = rng.randint(lo, hi)
        if kind == 1:
            keys.add(k)
        else:
            keys.discard(k)
        ops.append([kind, k])
    return ops


def small(rng):
    n = rng.randint(0, 6)
    root = fast_bst(rng, n, -9, 9, rng.choice(["random", "balanced", "sorted"]))
    keys = [v for v in root if v is not None]
    return {"root": root, "ops": make_ops(rng, keys, rng.randint(1, 4), -9, 9, "mixed")}


def build(rng, n, m, order="random", mix="mixed", lo=-10**5, hi=10**5):
    root = fast_bst(rng, n, lo, hi, order)
    keys = [v for v in root if v is not None]
    return {"root": root, "ops": make_ops(rng, keys, m, lo, hi, mix)}
