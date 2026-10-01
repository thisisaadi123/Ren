class Solution:
    def longestFresh(self, s):
        last = {}
        left = best = 0
        for i, c in enumerate(s):
            if last.get(c, -1) >= left:
                left = last[c] + 1
            last[c] = i
            best = max(best, i - left + 1)
        return best
