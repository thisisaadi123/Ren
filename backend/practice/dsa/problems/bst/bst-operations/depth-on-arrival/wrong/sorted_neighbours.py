class Solution:
    # Mistake: uses neighbours in the fully sorted order, not among keys that had already arrived.
    def arrivalDepths(self, keys):
        n = len(keys)
        order = sorted(range(n), key=keys.__getitem__)
        rank = [0] * n
        for r, i in enumerate(order):
            rank[i] = r
        depth = [0] * n
        for i in range(n):
            r = rank[i]
            c = [depth[order[s]] for s in (r - 1, r + 1) if 0 <= s < n and order[s] < i]
            depth[i] = (max(c) if c else 0) + 1
        return depth
