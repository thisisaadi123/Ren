class Solution:
    def countTargetStretches(self, nums, target):
        seen = collections.Counter({0: 1})
        total = prefix = 0
        for x in nums:
            prefix += x
            total += seen[prefix - target]
            seen[prefix] += 1
        return total
