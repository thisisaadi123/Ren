class Solution:
    # Mistake: only compares the totals, so ")(" looks balanced.
    def minInsertions(self, s):
        return abs(s.count("(") - s.count(")"))
