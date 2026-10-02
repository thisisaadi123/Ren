class Solution:
    def longestZigzag(self, root):
        nodes, stack = [], [root]
        while stack:
            n = stack.pop()
            nodes.append(n)
            stack += [c for c in (n.left, n.right) if c]
        best = 0
        for n in nodes:
            for first in ("L", "R"):
                cur, d, steps = n, first, 0
                while True:
                    nxt = cur.left if d == "L" else cur.right
                    if not nxt:
                        break
                    cur, steps = nxt, steps + 1
                    d = "R" if d == "L" else "L"
                best = max(best, steps)
        return best
