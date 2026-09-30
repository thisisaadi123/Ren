class Solution:
    def missingSeat(self, seats):
        n = len(seats)
        return n * (n + 1) // 2 - sum(seats)
