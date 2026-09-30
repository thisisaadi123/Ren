class Solution:
    def widestGap(self, nums):
        s = sorted(nums)
        return max((s[i + 1] - s[i] for i in range(len(s) - 1)), default=0)
