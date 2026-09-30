class Solution:
    def minAdjacentSwaps(self, heights):
        n = len(heights)
        return sum(1 for i in range(n) for j in range(i + 1, n) if heights[i] > heights[j])
