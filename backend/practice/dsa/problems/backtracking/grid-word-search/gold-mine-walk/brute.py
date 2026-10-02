class Solution:
    def mostGold(self, mine):
        m, n = len(mine), len(mine[0])
        best = 0
        stack = [((r, c), frozenset([(r, c)]), mine[r][c]) for r in range(m) for c in range(n) if mine[r][c]]
        while stack:
            (r, c), seen, total = stack.pop()
            best = max(best, total)
            for rr, cc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                if 0 <= rr < m and 0 <= cc < n and mine[rr][cc] and (rr, cc) not in seen:
                    stack.append(((rr, cc), seen | {(rr, cc)}, total + mine[rr][cc]))
        return best
