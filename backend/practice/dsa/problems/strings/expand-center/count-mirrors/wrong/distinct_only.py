class Solution:
    # Mistake: counts different palindromes, not positions.
    def countMirrors(self, s):
        n = len(s)
        seen = set()
        for c in range(2 * n - 1):
            i, j = c // 2, c // 2 + c % 2
            while i >= 0 and j < n and s[i] == s[j]:
                seen.add(s[i:j + 1])
                i -= 1
                j += 1
        return len(seen)
