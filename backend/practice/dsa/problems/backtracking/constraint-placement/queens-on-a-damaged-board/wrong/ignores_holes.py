class Solution:
    # Mistake: forgets the missing squares and counts placements on the full board.
    def countQueens(self, n, holes):
        cols, d1, d2 = set(), set(), set()
        def go(r):
            if r == n:
                return 1
            total = 0
            for c in range(n):
                if c in cols or r - c in d1 or r + c in d2:
                    continue
                cols.add(c); d1.add(r - c); d2.add(r + c)
                total += go(r + 1)
                cols.remove(c); d1.remove(r - c); d2.remove(r + c)
            return total
        return go(0)
