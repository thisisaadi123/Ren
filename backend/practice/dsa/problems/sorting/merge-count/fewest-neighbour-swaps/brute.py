class Solution:
    def minAdjacentSwaps(self, heights):
        a = heights[:]
        swaps = 0
        for i in range(len(a)):
            for j in range(len(a) - 1 - i):
                if a[j] > a[j + 1]:
                    a[j], a[j + 1] = a[j + 1], a[j]
                    swaps += 1
        return swaps
