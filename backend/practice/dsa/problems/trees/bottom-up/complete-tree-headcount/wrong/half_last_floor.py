class Solution:
    # Mistake: binary-searches the last floor but stops one seat early.
    def countNodes(self, root):
        if root is None:
            return 0
        h, x = 0, root
        while x.left:
            h += 1
            x = x.left
        if h == 0:
            return 1

        def exists(i):
            node = root
            for bit in range(h - 1, -1, -1):
                node = node.right if (i >> bit) & 1 else node.left
            return node is not None

        lo, hi = 0, (1 << h) - 1
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if exists(mid):
                lo = mid
            else:
                hi = mid - 1
        return (1 << h) - 1 + lo
