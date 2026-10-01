class Solution:
    # Mistake: updates cells in place one by one, so later cells see neighbours that already changed.
    def nextGeneration(self, board):
        g = [row[:] for row in board]
        m, n = len(g), len(g[0])
        for r in range(m):
            for c in range(n):
                live = 0
                for rr in range(max(0, r - 1), min(m, r + 2)):
                    for cc in range(max(0, c - 1), min(n, c + 2)):
                        if (rr, cc) != (r, c):
                            live += g[rr][cc]
                g[r][c] = 1 if live == 3 or (live == 2 and g[r][c]) else 0
        return g
