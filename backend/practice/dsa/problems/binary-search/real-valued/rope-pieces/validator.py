from ren_check import ints, integer
def validate(ropes, pieces):
    ints("ropes", ropes, 1, 10_000, 1, 10**7)
    integer("pieces", pieces, 1, 10**6)
