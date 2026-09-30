from ren_check import ints
def validate(pieces):
    ints("pieces", pieces, 1, 10_000, 0, 10**9)
