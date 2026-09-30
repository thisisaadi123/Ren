from ren_check import ints, integer
def validate(values, low, high):
    ints("values", values, 3, 1500, -10**6, 10**6)
    integer("low", low, -3 * 10**6, 3 * 10**6)
    integer("high", high, low, 3 * 10**6)
