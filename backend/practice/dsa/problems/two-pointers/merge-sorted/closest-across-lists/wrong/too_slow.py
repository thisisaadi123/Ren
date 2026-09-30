class Solution:
    def closestAcross(self, a, b):
        best = None
        for x in a:
            for y in b:
                d = abs(x - y)
                if best is None or d < best:
                    best = d
        return best
