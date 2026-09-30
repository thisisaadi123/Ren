class Solution:
    # Mistake: never looks beyond n.
    def firstMissing(self, nums, k):
        have = set(nums)
        return [x for x in range(1, len(nums) + 1) if x not in have][:k]
