class Solution:
    # Mistake: compares only the first and last reading of the window, not its max and min.
    def longestSteady(self, readings, limit):
        left = best = 0
        for i, v in enumerate(readings):
            while abs(v - readings[left]) > limit:
                left += 1
            best = max(best, i - left + 1)
        return best
