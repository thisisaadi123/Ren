class Solution:
    # Mistake: rejects phrases whose raw lengths differ, but spaces don't count.
    def isScramble(self, a, b):
        if len(a) != len(b):
            return False
        return sorted(a.replace(" ", "").lower()) == sorted(b.replace(" ", "").lower())
