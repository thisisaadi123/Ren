from ren_check import ints, integer
def validate(values, target):
    ints("values", values, 3, 1000, -1000, 1000)
    integer("target", target, -10**4, 10**4)
