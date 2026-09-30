class Solution:
    def rotateClockwise(self, photo):
        n = len(photo)
        return [[photo[n - 1 - c][r] for c in range(n)] for r in range(n)]
