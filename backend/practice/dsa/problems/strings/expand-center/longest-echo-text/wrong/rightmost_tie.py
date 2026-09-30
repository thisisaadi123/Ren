class Solution:
    # Mistake: on a tie keeps the later palindrome.
    def longestEchoText(self, s):
        n = len(s)
        best_i, best_len = 0, 1
        for c in range(2 * n - 1):
            i, j = c // 2, c // 2 + c % 2
            while i >= 0 and j < n and s[i] == s[j]:
                i -= 1
                j += 1
            if j - i - 1 >= best_len:
                best_i, best_len = i + 1, j - i - 1
        return s[best_i:best_i + best_len]
