class Solution:
    # Mistake: looks for t as a contiguous substring instead of a subsequence.
    def trailWindow(self, s, t):
        return t if t in s else ""
