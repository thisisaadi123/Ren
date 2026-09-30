from ren_check import ints
def validate(values):
    ints("values", values, 3, 2000, -10**5, 10**5)
