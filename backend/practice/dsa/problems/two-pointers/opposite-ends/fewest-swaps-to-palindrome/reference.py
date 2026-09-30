class Solution:
    def minSwapsToPalindrome(self, word):
        s = list(word)
        moves = 0
        while len(s) > 1:
            j = len(s) - 1
            while s[j] != s[0]:
                j -= 1
            if j == 0:
                # s[0] is the unpaired middle letter: it moves to the center later.
                moves += len(s) // 2
                s.pop(0)
            else:
                moves += len(s) - 1 - j
                s.pop(j)
                s.pop(0)
        return moves
