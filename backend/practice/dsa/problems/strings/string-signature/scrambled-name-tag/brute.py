class Solution:
    def isScramble(self, a, b):
        return sorted(a.replace(" ", "").lower()) == sorted(b.replace(" ", "").lower())
