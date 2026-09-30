class Solution:
    # Mistake: advances the pointer at the bigger value.
    def closestAcross(self, a, b):
        i = j = 0
        best = abs(a[0] - b[0])
        while i < len(a) and j < len(b):
            best = min(best, abs(a[i] - b[j]))
            if a[i] > b[j]:
                i += 1
            else:
                j += 1
        return best
