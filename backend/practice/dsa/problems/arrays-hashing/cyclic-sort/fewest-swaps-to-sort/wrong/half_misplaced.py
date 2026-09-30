class Solution:
    # Mistake: assumes every swap fixes two runners.
    def minSwaps(self, order):
        return (sum(1 for i, x in enumerate(order) if x != i + 1) + 1) // 2
