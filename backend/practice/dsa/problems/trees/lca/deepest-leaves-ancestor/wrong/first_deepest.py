class Solution:
    # Mistake: returns the first deepest node, ignoring the others.
    def deepestAncestor(self, root):
        level = [root]
        while True:
            nxt = [c for n in level for c in (n.left, n.right) if c]
            if not nxt:
                return level[0].val
            level = nxt
