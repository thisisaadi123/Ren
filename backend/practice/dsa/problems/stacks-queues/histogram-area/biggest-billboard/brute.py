class Solution:
    def biggestBillboard(self, heights):
        n = len(heights)
        return max(min(heights[a:b + 1]) * (b - a + 1) for a in range(n) for b in range(a, n))
