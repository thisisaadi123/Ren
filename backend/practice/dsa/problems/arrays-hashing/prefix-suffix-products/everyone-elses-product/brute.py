class Solution:
    def productOfOthers(self, nums):
        out = []
        for i in range(len(nums)):
            p = 1
            for j, x in enumerate(nums):
                if j != i:
                    p *= x
            out.append(p)
        return out
