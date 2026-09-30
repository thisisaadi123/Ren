class Solution:
    def closestPairSum(self, nums, target):
        n = len(nums)
        best = None
        for i in range(n):
            for j in range(i + 1, n):
                s = nums[i] + nums[j]
                if best is None or (abs(s - target), s) < (abs(best - target), best):
                    best = s
        return best
