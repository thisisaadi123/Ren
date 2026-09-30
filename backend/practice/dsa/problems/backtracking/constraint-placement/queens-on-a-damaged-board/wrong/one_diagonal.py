class Solution:
    # Mistake: checks the r - c diagonals but forgets the r + c ones.
    def countQueens(self, n, holes):
        hole = {(r, c) for r, c in holes}
        cols, d1 = set(), set()
        def go(r):
            if r == n:
                return 1
            total = 0
            for c in range(n):
                if c in cols or r - c in d1 or (r, c) in hole:
                    continue
                cols.add(c); d1.add(r - c)
                total += go(r + 1)
                cols.remove(c); d1.remove(r - c)
            return total
        return go(0)
