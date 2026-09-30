from fractions import Fraction
class Solution:
    def longestPiece(self, ropes, pieces):
        # The best length is always some rope cut into exactly j equal parts.
        best = Fraction(0)
        for r in ropes:
            for j in range(1, pieces + 1):
                L = Fraction(r, j)
                if L > best and sum(x // L for x in ropes) >= pieces:
                    best = L
        return float(best)
