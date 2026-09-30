class Solution:
    def countTargetStretches(self, nums, target):
        n = len(nums)
        return sum(sum(nums[i : j + 1]) == target for i in range(n) for j in range(i, n))
