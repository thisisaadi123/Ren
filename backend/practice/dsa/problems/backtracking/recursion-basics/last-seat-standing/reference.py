class Solution:
    def lastSeat(self, n, k):
        j = 0
        for size in range(2, n + 1):
            j = (j + k) % size
        return j + 1
