class Solution:
    # Mistake: only grows from single letters, so even echoes like "abba" are missed.
    def longestEcho(self, s):
        n = len(s)
        best = 1
        for c in range(n):
            i = j = c
            while i >= 0 and j < n and s[i] == s[j]:
                i -= 1
                j += 1
            best = max(best, j - i - 1)
        return best
