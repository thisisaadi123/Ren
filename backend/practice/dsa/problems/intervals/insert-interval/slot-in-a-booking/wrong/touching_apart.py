class Solution:
    # Mistake: leaves bookings that only touch the new one separate.
    def slotIn(self, bookings, extra):
        s, e = extra
        out, i, n = [], 0, len(bookings)
        while i < n and bookings[i][1] <= s:
            out.append(bookings[i])
            i += 1
        while i < n and bookings[i][0] < e:
            s, e = min(s, bookings[i][0]), max(e, bookings[i][1])
            i += 1
        out.append([s, e])
        out.extend(bookings[i:])
        return out
