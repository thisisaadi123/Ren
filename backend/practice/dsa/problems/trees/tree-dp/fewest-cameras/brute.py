class Solution:
    def fewestCameras(self, root):
        INF = float("inf")

        def go(t):
            # (camera here, watched by a child without a camera here, not watched yet)
            if not t:
                return INF, 0, 0
            a1, b1, c1 = go(t.left)
            a2, b2, c2 = go(t.right)
            cam = 1 + min(a1, b1, c1) + min(a2, b2, c2)
            kids = [k for k in ((a1, b1), (a2, b2))]
            base = sum(min(a, b) for a, b in kids)
            extra = min(a - min(a, b) for a, b in kids)
            covered = base + extra if extra < INF else INF
            open_ = min(a1, b1) + min(a2, b2)
            return cam, covered, open_

        a, b, _ = go(root)
        return min(a, b)
