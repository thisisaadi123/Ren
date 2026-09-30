class Solution:
    def minSwaps(self, order):
        a = order[:]
        swaps = 0
        for i in range(len(a)):
            if a[i] != i + 1:
                j = a.index(i + 1)
                a[i], a[j] = a[j], a[i]
                swaps += 1
        return swaps
