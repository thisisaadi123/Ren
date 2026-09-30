class Solution:
    # Mistake: ignores the ends, so a list that only climbs has no answer.
    def findSummit(self, heights):
        for i in range(1, len(heights) - 1):
            if heights[i - 1] < heights[i] > heights[i + 1]:
                return i
        return 0
