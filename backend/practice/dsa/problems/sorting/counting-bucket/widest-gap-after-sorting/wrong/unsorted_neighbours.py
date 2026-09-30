class Solution:
    # Mistake: measures neighbours in the original order.
    def widestGap(self, nums):
        return max((abs(nums[i + 1] - nums[i]) for i in range(len(nums) - 1)), default=0)
