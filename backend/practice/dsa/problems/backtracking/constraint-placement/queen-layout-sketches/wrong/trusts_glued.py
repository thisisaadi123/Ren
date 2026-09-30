class Solution:
    # Mistake: never checks the glued queens against each other; two glued queens in one row
    # silently become one, and clashing glued queens still give layouts.
    def queenLayouts(self, n, fixed):
        at = {}
        cols, d1, d2 = set(), set(), set()
        for r, c in fixed:
            at[r] = c
            cols.add(c); d1.add(r - c); d2.add(r + c)
        pos = [0] * n
        out = []
        def go(r):
            if r == n:
                out.append(["." * c + "Q" + "." * (n - c - 1) for c in pos])
                return
            if r in at:
                pos[r] = at[r]
                go(r + 1)
                return
            for c in range(n):
                if c in cols or r - c in d1 or r + c in d2:
                    continue
                cols.add(c); d1.add(r - c); d2.add(r + c)
                pos[r] = c
                go(r + 1)
                cols.remove(c); d1.remove(r - c); d2.remove(r + c)
        go(0)
        return out
