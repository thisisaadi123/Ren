class Solution:
    # Mistake: for every cell, walks left keeping the smallest column height: O(rows · cols²).
    def largestClearPlot(self, land):
        R, C = len(land), len(land[0])
        h = [0] * C
        best = 0
        for row in land:
            for c in range(C):
                h[c] = h[c] + 1 if row[c] == "1" else 0
            for c in range(C):
                low = h[c]
                k = c
                while k >= 0 and low:
                    low = min(low, h[k])
                    best = max(best, low * (c - k + 1))
                    k -= 1
        return best
