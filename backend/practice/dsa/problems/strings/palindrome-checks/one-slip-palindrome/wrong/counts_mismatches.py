class Solution:
    # Mistake: allows one mismatched pair, which fixes a changed letter, not an extra one.
    def oneSlip(self, s):
        bad = sum(1 for i in range(len(s) // 2) if s[i] != s[-1 - i])
        return bad <= 1
