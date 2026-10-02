class Solution:
    # Mistake: when one node is the other's ancestor, still steps up once more.
    def sharedAncestors(self, parent, queries):
        out = []
        for u, v in queries:
            seen = set()
            x = u
            while x != -1:
                seen.add(x)
                x = parent[x]
            y = v
            while y not in seen:
                y = parent[y]
            if (y == u or y == v) and u != v and parent[y] != -1:
                y = parent[y]
            out.append(y)
        return out
