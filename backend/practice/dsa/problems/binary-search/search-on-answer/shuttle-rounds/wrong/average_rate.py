class Solution:
    # Mistake: treats shuttles as if they could finish fractions of a round.
    def minTimeForRounds(self, roundTime, totalRounds):
        rate = sum(1 / t for t in roundTime)
        import math
        return math.ceil(totalRounds / rate)
