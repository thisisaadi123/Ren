class Solution:
    # Mistake: extends from every start, tracking max and min: O(n^2) when the limit is large.
    def longestSteady(self, readings, limit):
        n = len(readings)
        best = 0
        for i in range(n):
            mx = mn = readings[i]
            for j in range(i, n):
                v = readings[j]
                if v > mx:
                    mx = v
                if v < mn:
                    mn = v
                if mx - mn > limit:
                    break
                if j - i + 1 > best:
                    best = j - i + 1
        return best
