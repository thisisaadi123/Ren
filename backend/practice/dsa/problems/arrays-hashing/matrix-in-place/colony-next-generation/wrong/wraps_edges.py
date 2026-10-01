class Solution:
    # Mistake: treats the grid as wrapping around, so edge cells get neighbours from the far side.
    def nextGeneration(self, board):
        g = [row[:] for row in board]
        m, n = len(g), len(g[0])
        for r in range(m):
            for c in range(n):
                live = 0
                for dr in (-1, 0, 1):
                    for dc in (-1, 0, 1):
                        if dr or dc:
                            live += g[(r + dr) % m][(c + dc) % n] & 1
                if live == 3 or (live == 2 and g[r][c] & 1):
                    g[r][c] |= 2
        for row in g:
            for c in range(n):
                row[c] >>= 1
        return g
