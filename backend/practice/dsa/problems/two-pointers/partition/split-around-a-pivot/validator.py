from ren_check import ints, integer
def validate(values, pivot):
    ints("values", values, 1, 100_000, -10**6, 10**6)
    integer("pivot", pivot, -10**6, 10**6)
