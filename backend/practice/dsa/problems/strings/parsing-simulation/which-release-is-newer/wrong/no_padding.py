class Solution:
    # Mistake: compares the revision lists directly, so 1.0 looks newer than 1.
    def compareReleases(self, a, b):
        x = [int(r) for r in a.split(".")]
        y = [int(r) for r in b.split(".")]
        return (x > y) - (x < y)
