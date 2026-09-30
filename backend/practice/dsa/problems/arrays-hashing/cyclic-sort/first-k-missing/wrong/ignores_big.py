class Solution:
    # Mistake: past n, assumes every number is free.
    def firstMissing(self, nums, k):
        have = set(nums)
        n = len(nums)
        out = [x for x in range(1, n + 1) if x not in have][:k]
        x = n + 1
        while len(out) < k:
            out.append(x)
            x += 1
        return out
