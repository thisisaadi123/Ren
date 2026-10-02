class Solution:
    def ancestorJumps(self, parent, queries):
        out = []
        for v, k in queries:
            for _ in range(k):
                if v == -1:
                    break
                v = parent[v]
            out.append(v)
        return out
