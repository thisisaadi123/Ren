class Solution:
    # Mistake: scans every number for every query: O(n * q).
    def xorUnderCap(self, nums, queries):
        out = []
        for x, m in queries:
            best = -1
            for v in nums:
                if v <= m:
                    t = x ^ v
                    if t > best:
                        best = t
            out.append(best)
        return out
