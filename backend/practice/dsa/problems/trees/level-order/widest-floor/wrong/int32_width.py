class Solution:
    # Mistake: stores the width in a 32-bit integer.
    def widestFloor(self, root):
        best, level = 0, [(root, 0)]
        while level:
            first = level[0][1]
            w = (level[-1][1] - first + 1 + 2**31) % 2**32 - 2**31
            best = max(best, w)
            nxt = []
            for node, p in level:
                p -= first
                if node.left:
                    nxt.append((node.left, 2 * p))
                if node.right:
                    nxt.append((node.right, 2 * p + 1))
            level = nxt
        return best
