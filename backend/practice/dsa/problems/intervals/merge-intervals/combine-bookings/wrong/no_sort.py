class Solution:
    # Mistake: merges in the given order without sorting first.
    def combine(self, bookings):
        out = []
        for s, e in bookings:
            if out and s <= out[-1][1] and s >= out[-1][0]:
                out[-1][1] = max(out[-1][1], e)
            else:
                out.append([s, e])
        return out
