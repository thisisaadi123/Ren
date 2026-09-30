class Solution:
    # Mistake: counts misplaced runners instead of swaps.
    def minSwaps(self, order):
        return sum(1 for i, x in enumerate(order) if x != i + 1)
