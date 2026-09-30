class Solution:
    def countDivisiblePairs(self, nums, k):
        seen = collections.Counter()
        total = 0
        for x in nums:
            r = x % k
            total += seen[(k - r) % k]
            seen[r] += 1
        return total
