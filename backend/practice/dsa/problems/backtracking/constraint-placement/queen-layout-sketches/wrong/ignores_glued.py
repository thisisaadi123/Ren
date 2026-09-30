class Solution:
    # Mistake: returns every peaceful layout, glued queens or not.
    def queenLayouts(self, n, fixed):
        cols, d1, d2 = set(), set(), set()
        pos = [0] * n
        out = []
        def go(r):
            if r == n:
                out.append(["." * c + "Q" + "." * (n - c - 1) for c in pos])
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
