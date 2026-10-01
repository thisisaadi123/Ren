class Solution:
    def longestSteady(self, readings, limit):
        n = len(readings)
        best = 0
        for i in range(n):
            for j in range(i, n):
                part = readings[i:j + 1]
                if max(part) - min(part) <= limit:
                    best = max(best, j - i + 1)
        return best
