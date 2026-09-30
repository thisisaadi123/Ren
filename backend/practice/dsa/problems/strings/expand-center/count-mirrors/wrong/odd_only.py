class Solution:
    # Mistake: forgets the centers between two letters.
    def countMirrors(self, s):
        n = len(s)
        total = 0
        for c in range(n):
            i = j = c
            while i >= 0 and j < n and s[i] == s[j]:
                total += 1
                i -= 1
                j += 1
        return total
