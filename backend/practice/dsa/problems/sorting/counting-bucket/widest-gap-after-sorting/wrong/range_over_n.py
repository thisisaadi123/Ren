class Solution:
    # Mistake: returns the lower bound instead of the real gap.
    def widestGap(self, nums):
        if len(nums) < 2:
            return 0
        return -(-(max(nums) - min(nums)) // (len(nums) - 1))
