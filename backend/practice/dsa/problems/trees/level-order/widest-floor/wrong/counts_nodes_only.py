class Solution:
    # Mistake: counts the nodes on each floor and ignores the empty seats between them.
    def widestFloor(self, root):
        best, level = 0, [root]
        while level:
            best = max(best, len(level))
            level = [c for n in level for c in (n.left, n.right) if c]
        return best
