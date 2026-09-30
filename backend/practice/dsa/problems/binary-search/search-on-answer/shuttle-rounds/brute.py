class Solution:
    def minTimeForRounds(self, roundTime, totalRounds):
        t = 0
        while sum(t // r for r in roundTime) < totalRounds:
            t += 1
        return t
