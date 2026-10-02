class Solution:
    # Mistake: reads the tree level by level.
    def threadedInorder(self, root):
        out, level = [], [root] if root else []
        while level:
            out += [n.val for n in level]
            level = [c for n in level for c in (n.left, n.right) if c]
        return out
