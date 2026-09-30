class Solution:
    # Mistake: assumes there are no gaps below the maximum.
    def firstMissing(self, nums):
        pos = [x for x in nums if x > 0]
        return max(pos) + 1 if pos else 1
