class Solution:
    def findDoubleBooked(self, bookings):
        return sorted(set(v for v in bookings if bookings.count(v) == 2))
