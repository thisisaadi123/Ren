class Solution:
    def spiralOrder(self, grid):
        m, n = len(grid), len(grid[0])
        seen = [[False] * n for _ in range(m)]
        dr, dc = [0, 1, 0, -1], [1, 0, -1, 0]
        r = c = d = 0
        out = []
        for _ in range(m * n):
            out.append(grid[r][c]); seen[r][c] = True
            nr, nc = r + dr[d], c + dc[d]
            if not (0 <= nr < m and 0 <= nc < n and not seen[nr][nc]):
                d = (d + 1) % 4
                nr, nc = r + dr[d], c + dc[d]
            r, c = nr, nc
        return out
