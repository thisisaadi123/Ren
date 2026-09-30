from ren_check import ints
def validate(values):
    ints("values", values, 1, 100_000, 0, 100)
