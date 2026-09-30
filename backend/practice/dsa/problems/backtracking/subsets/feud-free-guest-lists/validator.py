from ren_check import ints, integer
def validate(ages, k):
    ints("ages", ages, 1, 18, 1, 1000)
    integer("k", k, 1, 1000)
