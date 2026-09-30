class Solution:
    def minSwaps(self, order):
        a = order[:]
        swaps = 0
        for i in range(len(a)):
            while a[i] != i + 1:
                j = a[i] - 1
                a[i], a[j] = a[j], a[i]
                swaps += 1
        return swaps
