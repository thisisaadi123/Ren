from ren_check import ints, integer
def validate(plays, k):
    ints("plays", plays, 1, 100_000, 0, 10**9)
    integer("k", k, 1, len(set(plays)))
