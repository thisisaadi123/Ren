from ren_check import ints
def validate(nums):
    ints("nums", nums, 2, 100_000, -2, 2)
    assert sum(1 for x in nums if abs(x) == 2) <= 60, "at most 60 elements may be 2 or -2"
