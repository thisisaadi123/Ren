from ren_check import ints, integer
def validate(roundTime, totalRounds):
    ints("roundTime", roundTime, 1, 100_000, 1, 10**7)
    integer("totalRounds", totalRounds, 1, 10**7)
