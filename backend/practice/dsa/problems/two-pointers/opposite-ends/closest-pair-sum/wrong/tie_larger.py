class Solution:
    # Mistake: keeps the larger sum on ties.
    def closestPairSum(self, nums, target):
        a = sorted(nums)
        i, j = 0, len(a) - 1
        best = None
        while i < j:
            s = a[i] + a[j]
            if best is None or (abs(s - target), -s) < (abs(best - target), -best):
                best = s
            if s < target:
                i += 1
            elif s > target:
                j -= 1
            else:
                return s
        return best
