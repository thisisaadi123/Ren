from ren_check import ints, integer
def validate(nums, target):
    ints("nums", nums, 2, 100_000, -10**9, 10**9)
    integer("target", target, -2 * 10**9, 2 * 10**9)
