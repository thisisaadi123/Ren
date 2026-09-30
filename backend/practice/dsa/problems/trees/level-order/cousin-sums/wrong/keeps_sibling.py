class Solution:
    # Mistake: subtracts only the node itself, so the sibling is counted as a cousin.
    def cousinSums(self, root):
        root.val = 0
        level = [root]
        while level:
            total = sum(c.val for n in level for c in (n.left, n.right) if c)
            nxt = [(c, total - c.val) for n in level for c in (n.left, n.right) if c]
            for c, v in nxt:
                c.val = v
            level = [c for c, _ in nxt]
        return root
