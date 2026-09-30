class Solution:
    # Mistake: one bubble pass only fixes neighbours.
    def sortLog(self, times, k):
        a = times[:]
        for j in range(len(a) - 1):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
        return a
