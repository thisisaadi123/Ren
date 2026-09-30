class Solution:
    # Mistake: counts the building itself as "ahead".
    def tallestAhead(self, heights):
        out = [0] * len(heights)
        best = -1
        for i in range(len(heights) - 1, -1, -1):
            best = max(best, heights[i])
            out[i] = best
        out[-1] = -1
        return out
