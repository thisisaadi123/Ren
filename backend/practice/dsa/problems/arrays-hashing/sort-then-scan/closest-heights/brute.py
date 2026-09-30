class Solution:
    def closestGap(self, heights):
        n = len(heights)
        return min(abs(heights[i] - heights[j]) for i in range(n) for j in range(i + 1, n))
