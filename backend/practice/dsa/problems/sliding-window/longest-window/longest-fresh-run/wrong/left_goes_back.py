class Solution:
    # Mistake: jumps left to the last copy + 1 even when that's behind the current left edge.
    def longestFresh(self, s):
        last = {}
        left = best = 0
        for i, c in enumerate(s):
            if c in last:
                left = last[c] + 1
            last[c] = i
            best = max(best, i - left + 1)
        return best
