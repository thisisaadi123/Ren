class Solution:
    # Mistake: divides the total product, which breaks when there's a zero.
    def productOfOthers(self, nums):
        total = 1
        for x in nums:
            total *= x
        return [total // x if x else 0 for x in nums]
