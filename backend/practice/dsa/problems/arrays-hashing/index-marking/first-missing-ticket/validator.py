from ren_check import ints
def validate(nums):
    ints("nums", nums, 1, 100_000, -2**31, 2**31 - 1)
