class Solution:
    # Mistake: tries every left end and extends right with a running minimum: O(n²).
    def biggestBillboard(self, heights):
        best, n = 0, len(heights)
        for a in range(n):
            low = heights[a]
            for b in range(a, n):
                low = min(low, heights[b])
                best = max(best, low * (b - a + 1))
        return best
