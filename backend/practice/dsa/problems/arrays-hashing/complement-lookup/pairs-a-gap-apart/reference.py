class Solution:
    def countGapPairs(self, nums, k):
        count = collections.Counter(nums)
        if k == 0:
            return sum(1 for c in count.values() if c > 1)
        return sum(1 for x in count if x + k in count)
