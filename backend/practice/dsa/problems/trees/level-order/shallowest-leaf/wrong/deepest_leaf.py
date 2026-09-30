class Solution:
    # Mistake: measures the longest route (the height) instead of the shortest.
    def shallowestLeaf(self, root):
        d, level = 0, [root] if root else []
        while level:
            d += 1
            level = [c for n in level for c in (n.left, n.right) if c]
        return d
