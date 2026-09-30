class Solution:
    # Mistake: forgets to reverse the suffix after the swap.
    def nextArrangement(self, values):
        a = values[:]
        n = len(a)
        i = n - 2
        while i >= 0 and a[i] >= a[i + 1]:
            i -= 1
        if i < 0:
            return sorted(a)
        j = n - 1
        while a[j] <= a[i]:
            j -= 1
        a[i], a[j] = a[j], a[i]
        return a
