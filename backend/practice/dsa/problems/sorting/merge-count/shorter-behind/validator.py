from ren_check import ints
def validate(heights):
    ints("heights", heights, 1, 100_000, -10**4, 10**4)
