class Solution:
    # Mistake: checks every later person with a running maximum; O(n²) when heights fall.
    def canSee(self, heights):
        n = len(heights)
        res = [0] * n
        for i in range(n):
            tallest = 0
            for j in range(i + 1, n):
                if tallest < min(heights[i], heights[j]):
                    res[i] += 1
                tallest = max(tallest, heights[j])
                if tallest >= heights[i]:
                    break
        return res
