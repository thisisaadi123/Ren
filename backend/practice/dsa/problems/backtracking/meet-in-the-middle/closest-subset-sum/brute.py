class Solution:
    def closestSubsetSum(self, nums, goal):
        sums = {0}
        for x in nums:
            sums |= {s + x for s in sums}
        return min(abs(s - goal) for s in sums)
