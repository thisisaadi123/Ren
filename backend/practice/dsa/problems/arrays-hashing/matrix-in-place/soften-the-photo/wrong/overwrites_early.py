class Solution:
    # Mistake: writes each average straight back, so later pixels average already-softened values.
    def soften(self, image):
        g = [row[:] for row in image]
        m, n = len(g), len(g[0])
        for r in range(m):
            for c in range(n):
                cells = [g[rr][cc] for rr in range(max(0, r - 1), min(m, r + 2))
                         for cc in range(max(0, c - 1), min(n, c + 2))]
                g[r][c] = sum(cells) // len(cells)
        return g
