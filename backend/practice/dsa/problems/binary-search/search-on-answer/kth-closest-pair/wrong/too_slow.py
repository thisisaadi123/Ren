class Solution:
    def kthPairGap(self, heights, k):
        n = len(heights)
        return sorted(abs(heights[i] - heights[j]) for i in range(n) for j in range(i + 1, n))[k - 1]
