class Solution:
    def bestXor(self, nums):
        return max(a ^ b for a in nums for b in nums)
