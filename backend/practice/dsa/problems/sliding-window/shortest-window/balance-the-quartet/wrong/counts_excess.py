class Solution:
    # Mistake: returns how many singers are over the quota, as if they could be fixed one by one.
    def shortestFix(self, s):
        q = len(s) // 4
        return sum(max(0, s.count(c) - q) for c in "SATB")
