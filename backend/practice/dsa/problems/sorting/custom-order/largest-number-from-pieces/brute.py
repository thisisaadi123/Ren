import itertools
class Solution:
    def largestNumber(self, pieces):
        best = max(int("".join(map(str, p))) for p in itertools.permutations(pieces))
        return str(best)
