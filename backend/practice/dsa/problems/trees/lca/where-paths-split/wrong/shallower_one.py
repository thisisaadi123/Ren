class Solution:
    # Mistake: assumes one of p and q always manages the other, and returns the shallower one.
    def splitPoint(self, root, p, q):
        level, depth = [root], {}
        d = 0
        while level:
            for n in level:
                depth[n.val] = d
            level = [c for n in level for c in (n.left, n.right) if c]
            d += 1
        return p if depth[p] <= depth[q] else q
