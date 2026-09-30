class Solution:
    # Mistake: reverses the rows before transposing, which rotates the other way.
    def rotateClockwise(self, photo):
        n = len(photo)
        for row in photo:
            row.reverse()
        for r in range(n):
            for c in range(r + 1, n):
                photo[r][c], photo[c][r] = photo[c][r], photo[r][c]
        return photo
