import collections
class Solution:
    def keepAtMostTwo(self, values):
        out = []
        for x, c in sorted(collections.Counter(values).items()):
            out += [x] * min(c, 2)
        return out
