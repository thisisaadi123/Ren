class Solution:
    # Mistake: counts mismatched mirror pairs instead of moves.
    def minSwapsToPalindrome(self, word):
        n = len(word)
        return sum(1 for i in range(n // 2) if word[i] != word[n - 1 - i])
