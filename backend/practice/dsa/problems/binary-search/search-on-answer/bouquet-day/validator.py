from ren_check import ints, integer
def validate(bloom, bouquets, size):
    ints("bloom", bloom, 1, 100_000, 1, 10**9)
    integer("bouquets", bouquets, 1, 10**6)
    integer("size", size, 1, len(bloom))
