class Solution:
    # Mistake: for k = 0, counts every value (x - x = 0) even if it appears once.
    def countGapPairs(self, nums, k):
        values = set(nums)
        return sum(1 for x in values if x + k in values)
