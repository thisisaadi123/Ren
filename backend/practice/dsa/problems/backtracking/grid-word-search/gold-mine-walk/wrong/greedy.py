class Solution:
    # Mistake: always steps to the richest neighbour instead of trying them all.
    def mostGold(self, mine):
        m, n = len(mine), len(mine[0])
        best = 0
        for r0 in range(m):
            for c0 in range(n):
                if not mine[r0][c0]:
                    continue
                seen, r, c, total = {(r0, c0)}, r0, c0, mine[r0][c0]
                while True:
                    opts = [(mine[rr][cc], rr, cc) for rr, cc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)) if 0 <= rr < m and 0 <= cc < n and mine[rr][cc] and (rr, cc) not in seen]
                    if not opts:
                        break
                    g, r, c = max(opts)
                    seen.add((r, c))
                    total += g
                best = max(best, total)
        return best
