class Solution:
    def bestTrail(self, root):
        nodes, parent, stack = [], [], [(root, -1)]
        while stack:
            n, p = stack.pop()
            parent.append(p)
            me = len(nodes)
            nodes.append(n.val)
            stack += [(c, me) for c in (n.left, n.right) if c]

        def up(i):
            out = []
            while i != -1:
                out.append(i)
                i = parent[i]
            return out

        best = None
        for a in range(len(nodes)):
            pa = up(a)
            for b in range(a, len(nodes)):
                pb = up(b)
                common = set(pa) & set(pb)
                path = [x for x in pa if x not in common] + [x for x in pb if x not in common]
                top = next(x for x in pa if x in common)
                s = sum(nodes[x] for x in path) + nodes[top]
                best = s if best is None else max(best, s)
        return best
