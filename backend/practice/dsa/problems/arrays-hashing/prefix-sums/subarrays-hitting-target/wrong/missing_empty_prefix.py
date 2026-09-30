class Solution:
    # Mistake: forgets the empty prefix, so stretches starting at index 0 are missed.
    def countTargetStretches(self, nums, target):
        seen = collections.Counter()
        total = prefix = 0
        for x in nums:
            prefix += x
            total += seen[prefix - target]
            seen[prefix] += 1
        return total
