class Solution:
    # Mistake: only looks at runs within one row or one column.
    def largestClearPlot(self, land):
        R, C = len(land), len(land[0])
        best = 0
        for row in land:
            run = 0
            for x in row:
                run = run + 1 if x == "1" else 0
                best = max(best, run)
        for c in range(C):
            run = 0
            for r in range(R):
                run = run + 1 if land[r][c] == "1" else 0
                best = max(best, run)
        return best
