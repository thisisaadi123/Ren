class Solution:
    # Mistake: compares revisions as text after dropping leading zeros, so 10 looks older than 9.
    def compareReleases(self, a, b):
        x = [r.lstrip("0") for r in a.split(".")]
        y = [r.lstrip("0") for r in b.split(".")]
        size = max(len(x), len(y))
        x += [""] * (size - len(x))
        y += [""] * (size - len(y))
        for p, q in zip(x, y):
            if p != q:
                return 1 if p > q else -1
        return 0
