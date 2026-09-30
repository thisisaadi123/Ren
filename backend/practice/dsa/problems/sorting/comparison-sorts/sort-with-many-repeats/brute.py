class Solution:
    def sortReadings(self, readings):
        a = readings[:]
        for i in range(len(a)):
            m = min(range(i, len(a)), key=a.__getitem__)
            a[i], a[m] = a[m], a[i]
        return a
