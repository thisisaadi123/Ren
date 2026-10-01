class Solution:
    def stepBack(self, ratings):
        a = ratings[:]
        i = len(a) - 2
        while i >= 0 and a[i] <= a[i + 1]:
            i -= 1
        if i < 0:
            return a[::-1]
        j = len(a) - 1
        while a[j] >= a[i]:
            j -= 1
        a[i], a[j] = a[j], a[i]
        a[i + 1:] = a[i + 1:][::-1]
        return a
