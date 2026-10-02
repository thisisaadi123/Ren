class Solution:
    # Mistake: counts overlapping neighbours after sorting by start.
    def cancelFewest(self, talks):
        t = sorted(talks)
        return sum(1 for a, b in zip(t, t[1:]) if b[0] < a[1])
