class Solution:
    # Mistake: starts right to left on floor 0, so every floor after it is flipped the wrong way.
    def zigzagFloors(self, root):
        out, level = [], [root] if root else []
        while level:
            vals = [n.val for n in level]
            out.append(vals if len(out) % 2 else vals[::-1])
            level = [c for n in level for c in (n.left, n.right) if c]
        return out
