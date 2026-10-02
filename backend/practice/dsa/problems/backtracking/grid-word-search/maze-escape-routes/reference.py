class Solution:
    def escapeRoutes(self, maze):
        m, n = len(maze), len(maze[0])
        seen = [[False] * n for _ in range(m)]

        def go(r, c):
            if (r, c) == (m - 1, n - 1):
                return 1
            seen[r][c] = True
            total = 0
            for rr, cc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                if 0 <= rr < m and 0 <= cc < n and not seen[rr][cc] and maze[rr][cc] == 0:
                    total += go(rr, cc)
            seen[r][c] = False
            return total

        return go(0, 0)
