from ren_check import ints, integer
def validate(nums, k):
    ints("nums", nums, 1, 100_000, 0, 10**9)
    integer("k", k, 1, 100_000)
