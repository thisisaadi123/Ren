class Solution:
    def countInRange(self, scores, queries):
        return [sum(lo <= x <= hi for x in scores) for lo, hi in queries]
