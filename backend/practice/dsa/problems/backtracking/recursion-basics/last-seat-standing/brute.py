class Solution:
    def lastSeat(self, n, k):
        seats, at = list(range(1, n + 1)), 0
        while len(seats) > 1:
            at = (at + k - 1) % len(seats)
            seats.pop(at)
        return seats[0]
