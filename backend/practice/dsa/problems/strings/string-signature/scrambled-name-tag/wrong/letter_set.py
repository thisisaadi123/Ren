class Solution:
    # Mistake: compares which letters appear, not how many times.
    def isScramble(self, a, b):
        return set(a.replace(" ", "").lower()) == set(b.replace(" ", "").lower())
