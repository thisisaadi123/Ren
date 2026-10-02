class Solution:
    # Mistake: only moves right or down.
    def escapeRoutes(self, maze):
        m, n = len(maze), len(maze[0])

        def go(r, c):
            if r >= m or c >= n or maze[r][c]:
                return 0
            if (r, c) == (m - 1, n - 1):
                return 1
            return go(r + 1, c) + go(r, c + 1)

        return go(0, 0)
