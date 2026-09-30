class Solution:
    def keepAtMostTwo(self, values):
        a = values[:]
        w = 0
        for x in values:
            if w < 2 or x != a[w - 2]:
                a[w] = x
                w += 1
        return a[:w]
