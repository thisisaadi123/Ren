class Solution:
    # Mistake: skips matching the outer ends, so it only keeps a palindromic prefix or suffix of the whole string.
    def shortestCut(self, s):
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
        return len(s) - max(pal_prefix(s), pal_prefix(s[::-1]))
