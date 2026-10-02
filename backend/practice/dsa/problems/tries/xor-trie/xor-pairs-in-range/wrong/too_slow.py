class Solution:
    # Mistake: checks every pair: O(n^2).
    def xorPairsInRange(self, nums, low, high):
        n = len(nums)
        total = 0
        for i in range(n):
            a = nums[i]
            for j in range(i + 1, n):
                v = a ^ nums[j]
                if low <= v <= high:
                    total += 1
        return total
