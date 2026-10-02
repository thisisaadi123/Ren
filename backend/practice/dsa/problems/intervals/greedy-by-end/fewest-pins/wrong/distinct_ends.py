class Solution:
    # Mistake: one pin per distinct end point.
    def fewestPins(self, posters):
        return len({e for _, e in posters})
