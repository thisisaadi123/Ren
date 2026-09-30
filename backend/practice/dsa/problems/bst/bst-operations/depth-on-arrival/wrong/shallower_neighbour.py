class Solution:
    # Mistake: hangs the new key under the shallower of its two neighbours.
    def arrivalDepths(self, keys):
        n = len(keys)
        order = sorted(range(n), key=keys.__getitem__)
        rank = [0] * n
        for r, i in enumerate(order):
            rank[i] = r
        prv = list(range(-1, n - 1))
        nxt = list(range(1, n + 1))
        below, above = [-1] * n, [-1] * n
        for i in range(n - 1, -1, -1):
            r = rank[i]
            p, q = prv[r], nxt[r]
            below[i] = order[p] if p >= 0 else -1
            above[i] = order[q] if q < n else -1
            if p >= 0:
                nxt[p] = q
            if q < n:
                prv[q] = p
        depth = [0] * n
        for i in range(n):
            c = [depth[j] for j in (below[i], above[i]) if j >= 0]
            depth[i] = (min(c) if c else 0) + 1
        return depth
