class Solution:
    # Mistake: only compares the tallest single building with the full-width billboard.
    def biggestBillboard(self, heights):
        return max(max(heights), min(heights) * len(heights))
