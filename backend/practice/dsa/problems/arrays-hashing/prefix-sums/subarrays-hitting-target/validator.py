from ren_check import ints, integer
def validate(nums, target):
    ints("nums", nums, 1, 100_000, -1000, 1000)
    integer("target", target, -10**7, 10**7)
