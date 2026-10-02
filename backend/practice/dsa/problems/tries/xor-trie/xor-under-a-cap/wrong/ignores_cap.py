class Solution:
    # Mistake: ignores the cap m.
    def xorUnderCap(self, nums, queries):
        return [max(x ^ v for v in nums) for x, m in queries]
