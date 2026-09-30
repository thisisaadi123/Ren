from ren_check import ints
import collections
def validate(bookings):
    ints("bookings", bookings, 1, 100_000, 1, len(bookings))
    assert max(collections.Counter(bookings).values()) <= 2, "each room appears at most twice"
