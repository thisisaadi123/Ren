class Solution:
    def tallestAhead(self, heights):
        n = len(heights)
        out = []
        for i in range(n):
            best = -1
            for j in range(i + 1, n):
                if heights[j] > best:
                    best = heights[j]
            out.append(best)
        return out
