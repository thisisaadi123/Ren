class Solution:
    def sharedAncestors(self, parent, queries):
        n = len(parent)
        kids = [[] for _ in range(n)]
        for v in range(1, n):
            kids[parent[v]].append(v)
        depth = [0] * n
        stack = [0]
        while stack:
            x = stack.pop()
            for c in kids[x]:
                depth[c] = depth[x] + 1
                stack.append(c)
        LOG = max(1, n.bit_length())
        up = [[p if p != -1 else 0 for p in parent]]
        for _ in range(1, LOG):
            prev = up[-1]
            up.append([prev[prev[v]] for v in range(n)])
        out = []
        for u, v in queries:
            if depth[u] < depth[v]:
                u, v = v, u
            d, j = depth[u] - depth[v], 0
            while d:
                if d & 1:
                    u = up[j][u]
                d >>= 1
                j += 1
            if u != v:
                for j in range(LOG - 1, -1, -1):
                    if up[j][u] != up[j][v]:
                        u, v = up[j][u], up[j][v]
                u = parent[u]
            out.append(u)
        return out
