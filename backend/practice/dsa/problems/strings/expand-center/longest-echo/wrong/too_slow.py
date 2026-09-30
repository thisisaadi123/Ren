class Solution:
    # Checks every substring by building it: O(n^3).
    def longestEcho(self, s):
        n = len(s)
        best = 0
        for i in range(n):
            for j in range(i + 1, n + 1):
                t = s[i:j]
                ok = True
                for k in range(len(t) // 2):
                    if t[k] != t[-1 - k]:
                        ok = False
                        break
                if ok:
                    best = max(best, j - i)
        return best
