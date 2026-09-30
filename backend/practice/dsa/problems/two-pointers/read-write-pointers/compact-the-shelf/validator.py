from ren_check import ints
def validate(slots):
    ints("slots", slots, 1, 100_000, -10**9, 10**9)
