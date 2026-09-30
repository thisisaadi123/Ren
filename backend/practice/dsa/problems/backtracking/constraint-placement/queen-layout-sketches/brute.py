import itertools
class Solution:
    def queenLayouts(self, n, fixed):
        out = []
        for p in itertools.permutations(range(n)):
            if len({r - p[r] for r in range(n)}) < n or len({r + p[r] for r in range(n)}) < n:
                continue
            if all(p[r] == c for r, c in fixed):
                out.append(["".join("Q" if p[r] == c else "." for c in range(n)) for r in range(n)])
        return out
