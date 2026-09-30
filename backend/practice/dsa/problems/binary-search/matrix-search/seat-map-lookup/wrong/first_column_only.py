class Solution:
    # Mistake: picks the row by its first value but then only checks that first value.
    def hasSeat(self, rows, target):
        firsts = [r[0] for r in rows]
        i = bisect.bisect_right(firsts, target) - 1
        return i >= 0 and rows[i][0] == target
