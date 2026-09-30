class Solution:
    def rotateClockwise(self, photo):
        n = len(photo)
        for r in range(n):
            for c in range(r + 1, n):
                photo[r][c], photo[c][r] = photo[c][r], photo[r][c]
        for row in photo:
            row.reverse()
        return photo
