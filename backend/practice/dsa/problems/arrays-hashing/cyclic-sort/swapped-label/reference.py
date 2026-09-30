class Solution:
    def findMislabel(self, labels):
        a = labels[:]
        i = 0
        while i < len(a):
            j = a[i] - 1
            if a[i] != a[j]:
                a[i], a[j] = a[j], a[i]
            else:
                i += 1
        for i, x in enumerate(a):
            if x != i + 1:
                return [x, i + 1]
        return [-1, -1]
