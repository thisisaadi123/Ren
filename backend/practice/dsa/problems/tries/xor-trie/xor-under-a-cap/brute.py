class Solution:
    def xorUnderCap(self, nums, queries):
        return [max((x ^ v for v in nums if v <= m), default=-1) for x, m in queries]
