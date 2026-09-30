from ren_check import ints, integer
def validate(weights, limit):
    integer("limit", limit, 1, 30_000)
    ints("weights", weights, 1, 100_000, 1, limit)
