class Solution:
    def zigzagFloors(self, root):
        out, level = [], [root] if root else []
        while level:
            vals = [n.val for n in level]
            out.append(vals[::-1] if len(out) % 2 else vals)
            level = [c for n in level for c in (n.left, n.right) if c]
        return out
