from ren_check import ints
def validate(votes):
    ints("votes", votes, 1, 100_000, -10**9, 10**9)
