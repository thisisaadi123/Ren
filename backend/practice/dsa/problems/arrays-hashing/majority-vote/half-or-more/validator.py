from ren_check import ints
def validate(votes):
    ints("votes", votes, 1, 100_000, 0, 10**9)
