class Solution:
    # Mistake: swaps with the FIRST copy of the largest smaller value, so the tail isn't ascending any more.
    def stepBack(self, ratings):
        a = ratings[:]
        i = len(a) - 2
        while i >= 0 and a[i] <= a[i + 1]:
            i -= 1
        if i < 0:
            return a[::-1]
        best = max(v for v in a[i + 1:] if v < a[i])
        j = a.index(best, i + 1)
        a[i], a[j] = a[j], a[i]
        a[i + 1:] = a[i + 1:][::-1]
        return a
