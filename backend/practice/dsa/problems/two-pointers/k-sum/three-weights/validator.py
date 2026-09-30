from ren_check import ints, integer
def validate(weights, target):
    ints("weights", weights, 3, 500, 1, 10**5)
    integer("target", target, 1, 3 * 10**5)
