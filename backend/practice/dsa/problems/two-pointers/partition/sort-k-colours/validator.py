from ren_check import ints, integer
def validate(balls, k):
    integer("k", k, 1, len(balls))
    ints("balls", balls, 1, 100_000, 1, k)
