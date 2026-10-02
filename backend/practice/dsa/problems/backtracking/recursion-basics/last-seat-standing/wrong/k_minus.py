class Solution:
    # Mistake: counts k − 1 places instead of k.
    def lastSeat(self, n, k):
        j = 0
        for size in range(2, n + 1):
            j = (j + k - 1) % size
        return j + 1
