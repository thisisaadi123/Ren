from ren_check import ints
def validate(heights):
    ints("heights", heights, 2, 100_000, 0, 10**9)
