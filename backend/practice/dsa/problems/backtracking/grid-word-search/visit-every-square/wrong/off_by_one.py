class Solution:
    # Mistake: forgets to count the start square, so tours are never complete.
    def tourCount(self, floor):
        m, n = len(floor), len(floor[0])
        need = sum(1 for r in floor for v in r if v == 0)
        sr, sc = next((r, c) for r in range(m) for c in range(n) if floor[r][c] == 1)
        seen = [[False] * n for _ in range(m)]

        def go(r, c, steps):
            if floor[r][c] == 2:
                return 1 if steps == need else 0
            seen[r][c] = True
            t = sum(go(rr, cc, steps + 1) for rr, cc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)) if 0 <= rr < m and 0 <= cc < n and not seen[rr][cc] and floor[rr][cc] != -1)
            seen[r][c] = False
            return t

        return go(sr, sc, 1)
