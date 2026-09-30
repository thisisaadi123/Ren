class Solution:
    def compactShelf(self, slots):
        a = slots[:]
        w = 0
        for x in a:
            if x != 0:
                a[w] = x
                w += 1
        for i in range(w, len(a)):
            a[i] = 0
        return a
