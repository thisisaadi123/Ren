class Solution:
    def compareReleases(self, a, b):
        x = [int(r) for r in a.split(".")]
        y = [int(r) for r in b.split(".")]
        size = max(len(x), len(y))
        x += [0] * (size - len(x))
        y += [0] * (size - len(y))
        for p, q in zip(x, y):
            if p != q:
                return 1 if p > q else -1
        return 0
