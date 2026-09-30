class Solution:
    # Mistake: treats 'D' and 'd' as different letters.
    def isScramble(self, a, b):
        return sorted(a.replace(" ", "")) == sorted(b.replace(" ", ""))
