class Solution:
    def rotateRight(self, slots, k):
        a = slots[:]
        n = len(a)
        k %= n
        def rev(i, j):
            while i < j:
                a[i], a[j] = a[j], a[i]
                i += 1
                j -= 1
        rev(0, n - 1)
        rev(0, k - 1)
        rev(k, n - 1)
        return a
