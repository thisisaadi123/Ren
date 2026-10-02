class Solution:
    # Mistake: climbs both nodes together without first evening out their depths.
    def sharedAncestors(self, parent, queries):
        out = []
        for u, v in queries:
            while u != v:
                if u != -1:
                    u = parent[u]
                if v != -1:
                    v = parent[v]
                if u == -1 or v == -1:
                    u = v = 0
            out.append(u)
        return out
