class Solution:
    def arrivalDepths(self, keys):
        n = len(keys)
        order = sorted(range(n), key=keys.__getitem__)
        rank = [0] * n
        for r, i in enumerate(order):
            rank[i] = r
        # Doubly linked list over ranks; walking arrivals backwards, a key's neighbours are
        # its predecessor and successor among the keys that arrived before it.
        prv = list(range(-1, n - 1))
        nxt = list(range(1, n + 1))
        below = [-1] * n
        above = [-1] * n
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
            a = depth[below[i]] if below[i] >= 0 else 0
            b = depth[above[i]] if above[i] >= 0 else 0
            depth[i] = (a if a > b else b) + 1
        return depth
