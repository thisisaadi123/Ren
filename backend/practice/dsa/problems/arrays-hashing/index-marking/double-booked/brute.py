class Solution:
    def findDoubleBooked(self, bookings):
        return sorted(v for v, c in collections.Counter(bookings).items() if c == 2)
