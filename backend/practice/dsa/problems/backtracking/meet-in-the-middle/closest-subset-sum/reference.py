from bisect import bisect_left


class Solution:
    def closestSubsetSum(self, nums, goal):
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
            if j:
                best = min(best, abs(a + B[j - 1] - goal))
            if best == 0:
                return 0
        return best
