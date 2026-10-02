class Solution:
    # Mistake: when a jump would go past the root, stays at the root instead of answering -1.
    def ancestorJumps(self, parent, queries):
        n = len(parent)
        up = [[p if p != -1 else 0 for p in parent]]
        j = 1
        while (1 << j) <= n:
            prev = up[-1]
            up.append([prev[prev[v]] for v in range(n)])
            j += 1
        out = []
        for v, k in queries:
            j = 0
            while k:
                if k & 1 and j < len(up):
                    v = up[j][v]
                k >>= 1
                j += 1
            out.append(v)
        return out
