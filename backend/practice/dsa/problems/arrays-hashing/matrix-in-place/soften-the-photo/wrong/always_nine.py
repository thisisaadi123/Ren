class Solution:
    # Mistake: always divides by 9, even at the edges where fewer pixels exist.
    def soften(self, image):
        m, n = len(image), len(image[0])
        return [[sum(image[rr][cc] for rr in range(max(0, r - 1), min(m, r + 2))
                     for cc in range(max(0, c - 1), min(n, c + 2))) // 9
                 for c in range(n)] for r in range(m)]
