class Solution:
    # Mistake: compares neighbours without sorting first.
    def closestGap(self, heights):
        return min(abs(b - a) for a, b in zip(heights, heights[1:]))
