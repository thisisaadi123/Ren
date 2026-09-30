class Solution:
    # Mistake: moves each value home once, but doesn't keep swapping the value it displaced.
    def firstMissing(self, nums):
        n = len(nums)
        for i in range(n):
            if 1 <= nums[i] <= n:
                j = nums[i] - 1
                nums[i], nums[j] = nums[j], nums[i]
        for i in range(n):
            if nums[i] != i + 1:
                return i + 1
        return n + 1
