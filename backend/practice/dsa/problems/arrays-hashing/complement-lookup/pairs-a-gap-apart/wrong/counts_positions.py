class Solution:
    # Mistake: counts every matching position pair, not distinct value pairs.
    def countGapPairs(self, nums, k):
        count = collections.Counter(nums)
        if k == 0:
            return sum(c * (c - 1) // 2 for c in count.values())
        return sum(c * count.get(x + k, 0) for x, c in count.items())
