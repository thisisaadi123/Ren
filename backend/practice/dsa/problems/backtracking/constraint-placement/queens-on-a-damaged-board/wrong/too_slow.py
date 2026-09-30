import itertools
class Solution:
    # Tries every column order (n! of them) and checks each: 11! is about 4 × 10^7.
    def countQueens(self, n, holes):
        hole = {(r, c) for r, c in holes}
        count = 0
        for p in itertools.permutations(range(n)):
            if any((r, p[r]) in hole for r in range(n)):
                continue
            if len({r - p[r] for r in range(n)}) == n and len({r + p[r] for r in range(n)}) == n:
                count += 1
        return count
