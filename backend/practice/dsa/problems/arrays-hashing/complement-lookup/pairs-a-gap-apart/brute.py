class Solution:
    def countGapPairs(self, nums, k):
        pairs = set()
        n = len(nums)
        for i in range(n):
            for j in range(n):
                if i != j and nums[j] - nums[i] == k:
                    pairs.add((nums[i], nums[j]))
        return len(pairs)
