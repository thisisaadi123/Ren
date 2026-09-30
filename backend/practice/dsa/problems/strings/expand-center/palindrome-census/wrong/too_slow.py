class Solution:
    # Expand around every center: O(n^2) on "aaaa...".
    def palindromeCensus(self, s):
        n = len(s)
        total = 0
        for c in range(2 * n - 1):
            i, j = c // 2, c // 2 + c % 2
            while i >= 0 and j < n and s[i] == s[j]:
                total += 1
                i -= 1
                j += 1
        return total
