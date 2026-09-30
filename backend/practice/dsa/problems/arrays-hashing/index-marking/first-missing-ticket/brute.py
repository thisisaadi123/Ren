class Solution:
    def firstMissing(self, nums):
        seen = set(nums)
        k = 1
        while k in seen:
            k += 1
        return k
