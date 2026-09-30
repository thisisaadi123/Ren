class Solution:
    def productOfOthers(self, nums):
        out = []
        for i in range(len(nums)):
            p = 1
            for j in range(len(nums)):
                if j != i:
                    p *= nums[j]
            out.append(p)
        return out
