class Solution:
    def tallestAhead(self, heights):
        return [max(heights[i + 1:]) if i + 1 < len(heights) else -1 for i in range(len(heights))]
