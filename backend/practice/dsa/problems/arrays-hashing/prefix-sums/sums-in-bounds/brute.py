class Solution:
    def countSumsInBounds(self, nums, lower, upper):
        n = len(nums)
        return sum(lower <= sum(nums[i : j + 1]) <= upper for i in range(n) for j in range(i, n))
