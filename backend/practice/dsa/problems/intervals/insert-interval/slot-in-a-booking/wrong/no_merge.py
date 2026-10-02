class Solution:
    # Mistake: inserts the booking in order but never combines it with its neighbours.
    def slotIn(self, bookings, extra):
        return sorted(bookings + [list(extra)])
