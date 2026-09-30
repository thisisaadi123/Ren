class Solution:
    # Mistake: divides with integer division, dropping the fraction.
    def floorAverages(self, root):
        out, level = [], [root]
        while level:
            out.append(float(int(sum(n.val for n in level) / len(level))))
            level = [c for n in level for c in (n.left, n.right) if c]
        return out
