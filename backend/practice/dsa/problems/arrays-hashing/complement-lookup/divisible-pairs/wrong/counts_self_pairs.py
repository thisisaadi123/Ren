class Solution:
    # Mistake: adds the number before looking, so it pairs with itself.
    def countDivisiblePairs(self, nums, k):
        seen = collections.Counter()
        total = 0
        for x in nums:
            r = x % k
            seen[r] += 1
            total += seen[(k - r) % k]
        return total
