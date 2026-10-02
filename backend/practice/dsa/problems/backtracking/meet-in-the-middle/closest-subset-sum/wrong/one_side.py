class Solution:
    # Mistake: only checks the first sum at or above the target in the other half.
    def closestSubsetSum(self, nums, goal):
        from bisect import bisect_left

        def sums(xs):
            out = [0]
            for x in xs:
                out += [s + x for s in out]
            return out

        h = len(nums) // 2
        A, B = sums(nums[:h]), sorted(sums(nums[h:]))
        best = abs(goal)
        for a in A:
            j = bisect_left(B, goal - a)
            if j < len(B):
                best = min(best, abs(a + B[j] - goal))
        return best
