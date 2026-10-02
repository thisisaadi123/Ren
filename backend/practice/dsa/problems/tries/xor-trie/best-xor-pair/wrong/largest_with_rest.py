class Solution:
    # Mistake: assumes the best pair always includes the largest number.
    def bestXor(self, nums):
        top = max(nums)
        return max(top ^ x for x in nums)
