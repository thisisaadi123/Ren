class Solution:
    def widestFloor(self, root):
        best, level = 0, [(root, 0)]
        while level:
            first = level[0][1]
            best = max(best, level[-1][1] - first + 1)
            nxt = []
            for node, p in level:
                p -= first
                if node.left:
                    nxt.append((node.left, 2 * p))
                if node.right:
                    nxt.append((node.right, 2 * p + 1))
            level = nxt
        return best
