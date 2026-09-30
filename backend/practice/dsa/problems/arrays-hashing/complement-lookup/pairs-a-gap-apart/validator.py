from ren_check import ints, integer
def validate(nums, k):
    ints("nums", nums, 1, 100_000, -10**7, 10**7)
    integer("k", k, 0, 10**7)
