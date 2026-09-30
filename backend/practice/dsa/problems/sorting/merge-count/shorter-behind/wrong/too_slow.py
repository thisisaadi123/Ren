class Solution:
    def countShorterBehind(self, heights):
        n = len(heights)
        out = [0] * n
        for i in range(n):
            c = 0
            for j in range(i + 1, n):
                if heights[j] < heights[i]:
                    c += 1
            out[i] = c
        return out
