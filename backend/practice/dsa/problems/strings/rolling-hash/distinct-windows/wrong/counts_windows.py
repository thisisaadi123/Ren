class Solution:
    # Mistake: counts windows, not different strings.
    def distinctWindows(self, s, k):
        return len(s) - k + 1
