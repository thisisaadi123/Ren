class Solution:
    def slotIn(self, bookings, extra):
        out = []
        for s, e in sorted(bookings + [extra]):
            if out and s <= out[-1][1]:
                out[-1][1] = max(out[-1][1], e)
            else:
                out.append([s, e])
        return out
