class Solution:
    def shortestCut(self, s):
        n, l = len(s), 0
        while l < n - 1 - l and s[l] == s[n - 1 - l]:
            l += 1
        mid = s[l:n - l]
        if len(mid) <= 1:
            return 0

        def pal_prefix(t):
            u = t + "#" + t[::-1]
            pi = [0] * len(u)
            for i in range(1, len(u)):
                k = pi[i - 1]
                while k and u[i] != u[k]:
                    k = pi[k - 1]
                if u[i] == u[k]:
                    k += 1
                pi[i] = k
            return pi[-1]

        return len(mid) - max(pal_prefix(mid), pal_prefix(mid[::-1]))
