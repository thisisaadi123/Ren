from ren_check import ints
def validate(heights):
    ints("heights", heights, 1, 100_000, -2**31, 2**31 - 1)
    assert all(a != b for a, b in zip(heights, heights[1:])), "neighbouring heights differ"
