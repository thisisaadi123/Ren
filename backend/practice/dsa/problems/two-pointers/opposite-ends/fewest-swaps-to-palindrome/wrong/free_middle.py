class Solution:
    # Mistake: forgets that the unpaired middle letter costs moves to reach the center.
    def minSwapsToPalindrome(self, word):
        s = list(word)
        moves = 0
        while len(s) > 1:
            j = len(s) - 1
            while s[j] != s[0]:
                j -= 1
            if j == 0:
                s.pop(0)
                continue
            moves += len(s) - 1 - j
            s.pop(j)
            s.pop(0)
        return moves
