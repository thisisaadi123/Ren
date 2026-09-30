class Solution:
    def countSumsInBounds(self, nums, lower, upper):
        total = 0
        for i in range(len(nums)):
            s = 0
            for j in range(i, len(nums)):
                s += nums[j]
                if lower <= s <= upper:
                    total += 1
        return total
