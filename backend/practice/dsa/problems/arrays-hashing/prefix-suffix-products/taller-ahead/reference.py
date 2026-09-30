class Solution:
    def tallestAhead(self, heights):
        out = [-1] * len(heights)
        best = -1
        for i in range(len(heights) - 1, -1, -1):
            out[i] = best
            best = max(best, heights[i])
        return out
