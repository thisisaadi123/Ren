class Solution:
    def firstMissing(self, nums, k):
        out, x = [], 1
        while len(out) < k:
            if x not in nums:
                out.append(x)
            x += 1
        return out
