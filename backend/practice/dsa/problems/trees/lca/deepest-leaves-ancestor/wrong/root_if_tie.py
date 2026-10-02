class Solution:
    # Mistake: compares only the root's two subtree heights and then keeps the first deepest node.
    def deepestAncestor(self, root):
        def h(t):
            return 0 if not t else 1 + max(h(t.left), h(t.right))

        if h(root.left) == h(root.right):
            return root.val
        level = [root]
        while True:
            nxt = [c for n in level for c in (n.left, n.right) if c]
            if not nxt:
                return level[0].val
            level = nxt
