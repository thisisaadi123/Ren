class Solution:
    # Mistake: tries every pair: O(n^2).
    def bestXor(self, nums):
        best = 0
        n = len(nums)
        for i in range(n):
            a = nums[i]
            for j in range(i + 1, n):
                v = a ^ nums[j]
                if v > best:
                    best = v
        return best
