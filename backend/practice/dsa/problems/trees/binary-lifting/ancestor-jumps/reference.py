class Solution:
    def ancestorJumps(self, parent, queries):
        n = len(parent)
        up = [parent[:]]
        j = 1
        while (1 << j) <= n:
            prev = up[-1]
            up.append([prev[prev[v]] if prev[v] != -1 else -1 for v in range(n)])
            j += 1
        out = []
        for v, k in queries:
            j = 0
            while k and v != -1:
                if k & 1:
                    v = up[j][v] if j < len(up) else -1
                k >>= 1
                j += 1
            out.append(v)
        return out
