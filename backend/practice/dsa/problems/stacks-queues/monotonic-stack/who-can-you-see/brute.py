class Solution:
    def canSee(self, heights):
        n = len(heights)
        res = []
        for i in range(n):
            c = 0
            for j in range(i + 1, n):
                if all(heights[x] < min(heights[i], heights[j]) for x in range(i + 1, j)):
                    c += 1
            res.append(c)
        return res
