class Solution:
    # Mistake: counts distinct letters.
    def mostPieces(self, s):
        return len(set(s))
