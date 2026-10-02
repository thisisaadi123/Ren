class Solution:
    # Mistake: keeps the earliest-starting talk at each conflict.
    def cancelFewest(self, talks):
        cancel, free = 0, -1
        for s, e in sorted(talks):
            if s >= free:
                free = e
            else:
                cancel += 1
        return cancel
