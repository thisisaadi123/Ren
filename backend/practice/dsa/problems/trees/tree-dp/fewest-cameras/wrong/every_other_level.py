class Solution:
    # Mistake: puts cameras on every third level, starting one above the bottom of the tree.
    def fewestCameras(self, root):
        levels, cur = [], [root]
        while cur:
            levels.append(len(cur))
            cur = [c for n in cur for c in (n.left, n.right) if c]
        d = len(levels)
        return max(1, sum(levels[i] for i in range(d - 2, -1, -3)) + (1 if (d - 2) % 3 == 2 or d == 1 else 0))
