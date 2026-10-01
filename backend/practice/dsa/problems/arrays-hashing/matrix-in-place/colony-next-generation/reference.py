class Solution:
    def nextGeneration(self, board):
        g = [row[:] for row in board]
        m, n = len(g), len(g[0])
        for r in range(m):
            for c in range(n):
                live = 0
                for rr in range(max(0, r - 1), min(m, r + 2)):
                    for cc in range(max(0, c - 1), min(n, c + 2)):
                        live += g[rr][cc] & 1
                live -= g[r][c] & 1
                if live == 3 or (live == 2 and g[r][c] & 1):
                    g[r][c] |= 2
        for row in g:
            for c in range(n):
                row[c] >>= 1
        return g
