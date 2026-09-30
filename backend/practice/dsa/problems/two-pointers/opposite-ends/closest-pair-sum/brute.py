class Solution:
    def closestPairSum(self, nums, target):
        n = len(nums)
        sums = [nums[i] + nums[j] for i in range(n) for j in range(i + 1, n)]
        return min(sums, key=lambda s: (abs(s - target), s))
