class Solution:
    # Mistake: a sliding window assumes every number is positive.
    def countTargetStretches(self, nums, target):
        total = s = left = 0
        for right, x in enumerate(nums):
            s += x
            while s > target and left <= right:
                s -= nums[left]; left += 1
            if s == target:
                total += 1
        return total
