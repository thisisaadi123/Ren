class Solution:
    # Mistake: tries every subset of all 36 numbers.
    def closestSubsetSum(self, nums, goal):
        best = abs(goal)

        def go(i, s):
            nonlocal best
            if i == len(nums):
                best = min(best, abs(s - goal))
                return
            go(i + 1, s)
            go(i + 1, s + nums[i])

        go(0, 0)
        return best
