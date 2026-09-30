class Solution:
    # Mistake: forgets to sort first.
    def closestPairSum(self, nums, target):
        a = nums
        i, j = 0, len(a) - 1
        best = a[0] + a[-1]
        while i < j:
            s = a[i] + a[j]
            if (abs(s - target), s) < (abs(best - target), best):
                best = s
            if s < target:
                i += 1
            else:
                j -= 1
        return best
