from ren_check import ints, integer
def validate(values, cap):
    ints("values", values, 3, 2000, -10**4, 10**4)
    integer("cap", cap, -3 * 10**4, 3 * 10**4)
