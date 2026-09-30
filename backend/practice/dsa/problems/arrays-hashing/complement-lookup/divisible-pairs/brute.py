class Solution:
    def countDivisiblePairs(self, nums, k):
        n = len(nums)
        return sum((nums[i] + nums[j]) % k == 0 for i in range(n) for j in range(i + 1, n))
