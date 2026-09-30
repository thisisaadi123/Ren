class Solution:
    # Mistake: scans the sorted list but never checks the end, missing seat n.
    def missingSeat(self, seats):
        s = sorted(seats)
        for i, v in enumerate(s):
            if v != i:
                return i
        return 0
