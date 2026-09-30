from ren_check import ints
def validate(readings):
    ints("readings", readings, 1, 100_000, -10**9, 10**9)
    assert len(readings) % 2 == 1, "the number of readings must be odd"
