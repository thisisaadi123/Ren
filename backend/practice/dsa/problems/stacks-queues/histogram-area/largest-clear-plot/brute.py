class Solution:
    def largestClearPlot(self, land):
        R, C = len(land), len(land[0])
        best = 0
        for r1 in range(R):
            for r2 in range(r1, R):
                for c1 in range(C):
                    for c2 in range(c1, C):
                        if all(land[r][c] == "1" for r in range(r1, r2 + 1) for c in range(c1, c2 + 1)):
                            best = max(best, (r2 - r1 + 1) * (c2 - c1 + 1))
        return best
