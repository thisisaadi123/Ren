class Solution:
    def escapeRoutes(self, maze):
        m, n = len(maze), len(maze[0])
        count = 0
        stack = [((0, 0), frozenset([(0, 0)]))]
        while stack:
            (r, c), seen = stack.pop()
            if (r, c) == (m - 1, n - 1):
                count += 1
                continue
            for rr, cc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                if 0 <= rr < m and 0 <= cc < n and maze[rr][cc] == 0 and (rr, cc) not in seen:
                    stack.append(((rr, cc), seen | {(rr, cc)}))
        return count
