from ren_check import ints
import collections
def validate(readings):
    ints("readings", readings, 1, 100_000, -10**9, 10**9)
    value, count = collections.Counter(readings).most_common(1)[0]
    assert count * 2 > len(readings), "some value must appear more than half the time"
