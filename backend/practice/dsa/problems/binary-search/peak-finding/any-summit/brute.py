class Solution:
    def findSummit(self, heights):
        # Any summit is accepted; the tallest point is always one.
        return heights.index(max(heights))
