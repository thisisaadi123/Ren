class Solution:
    # Mistake: leaves out scores equal to hi.
    def countInRange(self, scores, queries):
        s = sorted(scores)
        return [bisect.bisect_left(s, hi) - bisect.bisect_left(s, lo) for lo, hi in queries]
