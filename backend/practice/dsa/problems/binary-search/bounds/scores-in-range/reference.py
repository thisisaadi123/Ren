class Solution:
    def countInRange(self, scores, queries):
        s = sorted(scores)
        return [bisect.bisect_right(s, hi) - bisect.bisect_left(s, lo) for lo, hi in queries]
