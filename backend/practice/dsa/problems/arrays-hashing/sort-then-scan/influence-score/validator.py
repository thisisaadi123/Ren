from ren_check import ints
def validate(citations):
    ints("citations", citations, 1, 100_000, 0, 10**9)
