class Solution:
    def sharedAncestors(self, parent, queries):
        out = []
        for u, v in queries:
            seen = set()
            while u != -1:
                seen.add(u)
                u = parent[u]
            while v not in seen:
                v = parent[v]
            out.append(v)
        return out
