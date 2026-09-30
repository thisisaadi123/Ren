from ren_check import ints
def validate(changes):
    ints("changes", changes, 1, 100_000, -10**4, 10**4)
