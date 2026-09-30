from ren_check import ints, integer
def validate(nums, lower, upper):
    ints("nums", nums, 1, 30_000, -2**31, 2**31 - 1)
    integer("lower", lower, -10**5, 10**5)
    integer("upper", upper, lower, 10**5)
