class Solution:
    def countTargetStretches(self, nums, target):
        total = 0
        for i in range(len(nums)):
            s = 0
            for j in range(i, len(nums)):
                s += nums[j]
                total += s == target
        return total
