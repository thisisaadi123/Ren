from ren_check import ints
def validate(readings):
    ints("readings", readings, 1, 100_000, 0, 10**9)
