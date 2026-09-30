class Solution:
    # Mistake: returns the repeats in the order they were found.
    def findDoubleBooked(self, bookings):
        twice = []
        for v in bookings:
            i = abs(v) - 1
            if bookings[i] < 0:
                twice.append(abs(v))
            else:
                bookings[i] = -bookings[i]
        return twice
