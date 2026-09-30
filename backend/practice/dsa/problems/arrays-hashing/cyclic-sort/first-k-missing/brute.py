class Solution:
    def firstMissing(self, nums, k):
        have = set(nums)
        out, x = [], 1
        while len(out) < k:
            if x not in have:
                out.append(x)
            x += 1
        return out
