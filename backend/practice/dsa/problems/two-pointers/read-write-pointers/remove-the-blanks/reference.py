class Solution:
    def removeValue(self, cells, blank):
        a = cells[:]
        w = 0
        for x in a:
            if x != blank:
                a[w] = x
                w += 1
        return a[:w]
