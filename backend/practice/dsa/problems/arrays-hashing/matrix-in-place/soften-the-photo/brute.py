class Solution:
    def soften(self, image):
        m, n = len(image), len(image[0])
        out = []
        for r in range(m):
            row = []
            for c in range(n):
                cells = [image[r + dr][c + dc] for dr in (-1, 0, 1) for dc in (-1, 0, 1)
                         if 0 <= r + dr < m and 0 <= c + dc < n]
                row.append(sum(cells) // len(cells))
            out.append(row)
        return out
