class Solution:
    # Mistake: talks that only touch count as overlapping.
    def cancelFewest(self, talks):
        cancel, free = 0, -1
        for s, e in sorted(talks, key=lambda t: t[1]):
            if s > free:
                free = e
            else:
                cancel += 1
        return cancel
