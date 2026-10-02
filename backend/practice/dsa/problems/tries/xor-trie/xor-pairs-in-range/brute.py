class Solution:
    def xorPairsInRange(self, nums, low, high):
        n = len(nums)
        return sum(1 for i in range(n) for j in range(i + 1, n) if low <= nums[i] ^ nums[j] <= high)
