from ren_gen import bst
import collections


def preorder(root):
    """Level-order BST -> preorder list of keys."""
    if not root:
        return []
    kids, vals = {}, [root[0]]
    q = collections.deque([0])
    i = 1
    while q and i < len(root):
        p = q.popleft()
        kids[p] = [None, None]
        for s in (0, 1):
            if i < len(root) and root[i] is not None:
                vals.append(root[i])
                kids[p][s] = len(vals) - 1
                q.append(len(vals) - 1)
            i += 1
    out, st = [], [0]
    while st:
        x = st.pop()
        out.append(vals[x])
        l, r = kids.get(x, [None, None])
        if r is not None:
            st.append(r)
        if l is not None:
            st.append(l)
    return out


def make(rng, n, lo, hi, order, broken, flip="desc"):
    if order == "sorted":
        seq = sorted(rng.sample(range(lo, hi + 1), n))
        if flip == "desc":
            seq.reverse()
    else:
        seq = preorder(bst(rng, n, lo, hi, order))
    if broken and n >= 3:
        how = rng.choice(["swap", "move", "late"])
        if how == "swap":
            i, j = rng.sample(range(n), 2)
            seq[i], seq[j] = seq[j], seq[i]
        elif how == "move":
            x = seq.pop(rng.randrange(n))
            seq.insert(rng.randrange(n), x)
        else:
            # a key near the end that falls just under a bound set far earlier
            i = rng.randrange(n // 2, n)
            x = seq.pop(i)
            seq.insert(rng.randrange(1, max(2, n // 4)), x)
    return seq


def small(rng):
    n = rng.randint(1, 8)
    return {"keys": make(rng, n, -20, 20, rng.choice(["random", "random", "balanced", "sorted"]),
                         rng.random() < 0.5, rng.choice(["asc", "desc"]))}


def build(rng, n, order="random", broken=False, flip="desc"):
    return {"keys": make(rng, n, -10**9, 10**9, order, broken, flip)}
