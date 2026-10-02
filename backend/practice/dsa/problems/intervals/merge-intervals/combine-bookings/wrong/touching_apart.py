class Solution:
    # Mistake: treats bookings that only touch as separate.
    def combine(self, bookings):
        out = []
        for s, e in sorted(bookings):
            if out and s < out[-1][1]:
                out[-1][1] = max(out[-1][1], e)
            else:
                out.append([s, e])
        return out
