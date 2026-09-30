class Solution:
    # Mistake: parses each revision into a 64-bit integer, which wraps for revisions over 19 digits.
    def compareReleases(self, a, b):
        def wrap(r):
            v = int(r) % (1 << 64)
            return v - (1 << 64) if v >= 1 << 63 else v
        x = [wrap(r) for r in a.split(".")]
        y = [wrap(r) for r in b.split(".")]
        size = max(len(x), len(y))
        x += [0] * (size - len(x))
        y += [0] * (size - len(y))
        for p, q in zip(x, y):
            if p != q:
                return 1 if p > q else -1
        return 0
