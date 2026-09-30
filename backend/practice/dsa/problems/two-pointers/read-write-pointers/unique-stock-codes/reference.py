class Solution:
    def uniqueSorted(self, codes):
        a = codes[:]
        w = 1
        for i in range(1, len(a)):
            if a[i] != a[w - 1]:
                a[w] = a[i]
                w += 1
        return a[:w]
