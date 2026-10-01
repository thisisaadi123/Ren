class Solution:
    # Mistake: rounds the average to the nearest whole number instead of down.
    def soften(self, image):
        m, n = len(image), len(image[0])
        out = []
        for r in range(m):
            row = []
            for c in range(n):
                cells = [image[rr][cc] for rr in range(max(0, r - 1), min(m, r + 2))
                         for cc in range(max(0, c - 1), min(n, c + 2))]
                row.append((2 * sum(cells) + len(cells)) // (2 * len(cells)))
            out.append(row)
        return out
