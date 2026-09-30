from ren_check import ints, integer
def validate(slots, k):
    ints("slots", slots, 1, 100_000, -10**9, 10**9)
    integer("k", k, 0, 10**9)
