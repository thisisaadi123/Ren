class Solution:
    # Mistake: only tries walks that start at the root.
    def longestZigzag(self, root):
        best = 0
        for first in ("L", "R"):
            cur, d, steps = root, first, 0
            while True:
                nxt = cur.left if d == "L" else cur.right
                if not nxt:
                    break
                cur, steps = nxt, steps + 1
                d = "R" if d == "L" else "L"
            best = max(best, steps)
        return best
