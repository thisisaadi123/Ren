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

from ren_gen import distinct


def keys_for(rng, n, lo, hi, kind):
    if kind == "symmetric":
        # many pairs: keys come in pairs x, T - x
        T = rng.randint(lo // 2, hi // 2)
        half = set()
        while len(half) < n // 2:
            x = rng.randint(lo, hi)
            if lo <= T - x <= hi and x != T - x:
                half.add(min(x, T - x))
        ks = set()
        for x in half:
            ks.add(x); ks.add(T - x)
        while len(ks) < n:
            ks.add(rng.randint(lo, hi))
        return sorted(ks)[:n] if len(ks) > n else sorted(ks), T
    ks = distinct(rng, n, lo, hi)
    return ks, None


def make(rng, n, lo, hi, order, kind, target):
    ks, T = keys_for(rng, n, lo, hi, kind)
    if order in ("sorted", "left-chain"):
        root = chain_bst(ks, left=(order == "left-chain"))
    else:
        # insert in a random or balanced order
        ks = sorted(ks)
        if order == "balanced":
            seq = []
            st = [(0, len(ks) - 1)]
            while st:
                a, b = st.pop()
                if a > b:
                    continue
                m = (a + b) // 2
                seq.append(ks[m]); st.append((a, m - 1)); st.append((m + 1, b))
        else:
            seq = ks[:]
            rng.shuffle(seq)
        vals, L, R = [seq[0]], [-1], [-1]
        for k in seq[1:]:
            cur = 0
            while True:
                side = L if k < vals[cur] else R
                if side[cur] == -1:
                    vals.append(k); L.append(-1); R.append(-1)
                    side[cur] = len(vals) - 1
                    break
                cur = side[cur]
        root = serialize(vals, L, R)
    if T is None:
        if target == "pair":
            a, b = rng.sample(ks, 2) if len(ks) > 1 else (ks[0], ks[0] + 1)
            T = a + b
        elif target == "double":
            T = 2 * rng.choice(ks)
        else:
            T = rng.randint(2 * lo, 2 * hi)
    return {"root": root, "target": max(-2 * 10**9, min(2 * 10**9, T))}


def small(rng):
    n = rng.randint(1, 8)
    return make(rng, n, -12, 12, rng.choice(["random", "balanced", "sorted"]),
                rng.choice(["plain", "symmetric"]) if n > 1 else "plain", rng.choice(["pair", "double", "any"]))


def build(rng, n, order="random", kind="plain", target="pair", lo=-10**9, hi=10**9):
    return make(rng, n, lo, hi, order, kind, target)
