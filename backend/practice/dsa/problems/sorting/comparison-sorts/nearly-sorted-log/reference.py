class Solution:
    def sortLog(self, times, k):
        a = times[:]
        for i in range(1, len(a)):
            x, j = a[i], i - 1
            while j >= 0 and a[j] > x:
                a[j + 1] = a[j]
                j -= 1
            a[j + 1] = x
        return a
