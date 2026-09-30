class Solution:
    def widestFloor(self, root):
        # Record every node's seat as a path of left/right turns, then compare per floor.
        seats = {}

        def walk(node, d, p):
            if node:
                lo, hi = seats.get(d, (p, p))
                seats[d] = (min(lo, p), max(hi, p))
                walk(node.left, d + 1, 2 * p)
                walk(node.right, d + 1, 2 * p + 1)

        walk(root, 0, 0)
        return max(hi - lo + 1 for lo, hi in seats.values())
