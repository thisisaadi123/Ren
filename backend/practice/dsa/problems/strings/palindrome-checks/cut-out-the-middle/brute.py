class Solution:
    def shortestCut(self, s):
        n = len(s)
        for size in range(n + 1):
            for i in range(n - size + 1):
                t = s[:i] + s[i + size:]
                if t == t[::-1]:
                    return size
