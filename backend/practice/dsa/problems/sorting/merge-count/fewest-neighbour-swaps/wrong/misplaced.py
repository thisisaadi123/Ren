class Solution:
    # Mistake: counts students out of place, not swaps.
    def minAdjacentSwaps(self, heights):
        return sum(1 for a, b in zip(heights, sorted(heights)) if a != b)
