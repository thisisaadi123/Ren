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

from ren_gen import bst

LO, HI = -2**31, 2**31 - 1


def make(rng, n, how, lo, hi, order):
    vals, L, R = parse(fast_bst(rng, n, lo, hi, order))
    ino = inorder(L, R)
    if how == "adjacent":
        k = rng.randrange(n - 1)
        i, j = ino[k], ino[k + 1]
    elif how == "ends":
        i, j = ino[0], ino[-1]
    elif how == "root":
        i, j = 0, rng.choice([x for x in range(n) if x != 0])
    else:
        i, j = rng.sample(range(n), 2)
    vals[i], vals[j] = vals[j], vals[i]
    return serialize(vals, L, R)


def small(rng):
    n = rng.randint(2, 7)
    return {"root": make(rng, n, rng.choice(["any", "adjacent", "ends", "root"]), -30, 30,
                         rng.choice(["random", "sorted", "balanced"]))}


def build(rng, n, how="any", order="random", wide=False):
    lo, hi = (LO, HI) if wide else (-10**6, 10**6)
    return {"root": make(rng, n, how, lo, hi, order)}
