class Solution:
    def soften(self, image):
        g = [row[:] for row in image]
        m, n = len(g), len(g[0])
        for r in range(m):
            for c in range(n):
                total = count = 0
                for rr in range(max(0, r - 1), min(m, r + 2)):
                    for cc in range(max(0, c - 1), min(n, c + 2)):
                        total += g[rr][cc] & 255
                        count += 1
                g[r][c] |= (total // count) << 8
        for row in g:
            for c in range(n):
                row[c] >>= 8
        return g
