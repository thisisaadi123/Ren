from ren_check import ints
def validate(heights):
    ints("heights", heights, 1, 100_000, 1, 10**9)
