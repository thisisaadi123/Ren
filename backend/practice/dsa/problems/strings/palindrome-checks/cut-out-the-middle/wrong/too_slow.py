class Solution:
    # Finds the longest palindromic prefix/suffix of the middle by trying every length: O(n²).
    def shortestCut(self, s):
        n, l = len(s), 0
        while l < n - 1 - l and s[l] == s[n - 1 - l]:
            l += 1
        mid = s[l:n - l]
        m = len(mid)
        if m <= 1:
            return 0

        def is_pal(t, a, b):
            while a < b:
                if t[a] != t[b]:
                    return False
                a += 1
                b -= 1
            return True

        best = 1
        for L in range(m, 1, -1):
            if is_pal(mid, 0, L - 1) or is_pal(mid, m - L, m - 1):
                best = L
                break
        return m - best
