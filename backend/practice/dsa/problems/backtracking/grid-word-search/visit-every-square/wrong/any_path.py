class Solution:
    # Mistake: counts every simple path to the end, even ones that skip squares.
    def tourCount(self, floor):
        m, n = len(floor), len(floor[0])
        sr, sc = next((r, c) for r in range(m) for c in range(n) if floor[r][c] == 1)
        seen = [[False] * n for _ in range(m)]

        def go(r, c):
            if floor[r][c] == 2:
                return 1
            seen[r][c] = True
            t = sum(go(rr, cc) for rr, cc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)) if 0 <= rr < m and 0 <= cc < n and not seen[rr][cc] and floor[rr][cc] != -1)
            seen[r][c] = False
            return t

        return go(sr, sc)
