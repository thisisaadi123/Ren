class Solution:
    def closestGap(self, heights):
        s = sorted(heights)
        return min(b - a for a, b in zip(s, s[1:]))
