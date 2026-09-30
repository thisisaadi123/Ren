class Solution:
    def missingSeat(self, seats):
        taken = set(seats)
        return next(i for i in range(len(seats) + 1) if i not in taken)
