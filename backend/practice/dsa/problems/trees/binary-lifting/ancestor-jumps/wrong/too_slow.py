class Solution:
    # Mistake: climbs one step at a time: O(k) per query, O(n * q) on a long chain.
    def ancestorJumps(self, parent, queries):
        out = []
        for v, k in queries:
            for _ in range(k):
                v = parent[v]
                if v == -1:
                    break
            out.append(v)
        return out
