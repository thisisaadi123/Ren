class Solution:
    def hasSeat(self, rows, target):
        return any(target in r for r in rows)
