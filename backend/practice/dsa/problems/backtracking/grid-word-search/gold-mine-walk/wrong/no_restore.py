class Solution:
    # Mistake: never puts the gold back, so later paths find cells already emptied.
    def mostGold(self, mine):
        m, n = len(mine), len(mine[0])

        def go(r, c):
            g = mine[r][c]
            mine[r][c] = 0
            best = 0
            for rr, cc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                if 0 <= rr < m and 0 <= cc < n and mine[rr][cc]:
                    best = max(best, go(rr, cc))
            return g + best

        return max((go(r, c) for r in range(m) for c in range(n) if mine[r][c]), default=0)
