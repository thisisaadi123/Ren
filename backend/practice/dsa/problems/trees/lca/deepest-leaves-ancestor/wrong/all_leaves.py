class Solution:
    # Mistake: finds the common ancestor of ALL leaves, not just the deepest ones.
    def deepestAncestor(self, root):
        def go(t):
            if not t:
                return 0, None
            if not t.left and not t.right:
                return 1, t.val
            cl, a = go(t.left)
            cr, b = go(t.right)
            if cl and cr:
                return cl + cr, t.val
            return (cl, a) if cl else (cr, b)

        return go(root)[1]
