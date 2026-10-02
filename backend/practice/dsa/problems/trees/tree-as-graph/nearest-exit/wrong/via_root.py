class Solution:
    # Mistake: when going up, only considers the root's nearest leaf, not branches on the way.
    def nearestExit(self, root, start):
        def nearest_below(t):
            level, d = [t], 0
            while True:
                hits = [n.val for n in level if not n.left and not n.right]
                if hits:
                    return d, min(hits)
                level = [c for n in level for c in (n.left, n.right) if c]
                d += 1

        stack, node, depth = [(root, 0)], None, 0
        while stack:
            n, d = stack.pop()
            if n.val == start:
                node, depth = n, d
                break
            stack += [(c, d + 1) for c in (n.left, n.right) if c]
        a = nearest_below(node)
        b = nearest_below(root)
        b = (b[0] + depth, b[1])
        return min(a, b)[1]
