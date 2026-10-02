class Solution:
    # Mistake: forgets that the empty subset (sum 0) is allowed.
    def closestSubsetSum(self, nums, goal):
        sums = set()
        for x in nums:
            sums |= {s + x for s in sums} | {x}
        return min(abs(s - goal) for s in sums)
