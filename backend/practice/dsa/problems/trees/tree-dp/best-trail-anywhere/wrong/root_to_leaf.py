class Solution:
    # Mistake: only considers trails from the root down to a leaf.
    def bestTrail(self, root):
        best, stack = None, [(root, root.val)]
        while stack:
            n, s = stack.pop()
            if not n.left and not n.right:
                best = s if best is None else max(best, s)
            stack += [(c, s + c.val) for c in (n.left, n.right) if c]
        return best
