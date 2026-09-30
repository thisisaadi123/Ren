class Solution:
    # Mistake: after matching the ends, cuts out the whole unmatched middle.
    def shortestCut(self, s):
        n, l = len(s), 0
        while l < n - 1 - l and s[l] == s[n - 1 - l]:
            l += 1
        mid = n - 2 * l
        return 0 if mid <= 1 else mid
