from ren_check import ints, integer
def validate(values, step):
    ints("values", values, 1, 100_000, -10**9, 10**9)
    integer("step", step, 1, 10**9)
