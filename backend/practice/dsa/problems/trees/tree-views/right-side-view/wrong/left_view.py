class Solution:
    # Mistake: reports the leftmost node of each level.
    def rightView(self, root):
        out, level = [], [root] if root else []
        while level:
            out.append(level[0].val)
            level = [c for n in level for c in (n.left, n.right) if c]
        return out
