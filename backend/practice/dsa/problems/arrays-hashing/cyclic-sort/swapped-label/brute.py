class Solution:
    def findMislabel(self, labels):
        n = len(labels)
        dup = next(x for x in range(1, n + 1) if labels.count(x) == 2)
        missing = next(x for x in range(1, n + 1) if x not in labels)
        return [dup, missing]
