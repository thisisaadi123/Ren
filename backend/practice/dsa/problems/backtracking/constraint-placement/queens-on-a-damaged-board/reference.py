class Solution:
    def countQueens(self, n, holes):
        blocked = [0] * n
        for r, c in holes:
            blocked[r] |= 1 << c
        full = (1 << n) - 1

        def go(r, cols, d1, d2):
            if r == n:
                return 1
            free = full & ~(cols | d1 | d2 | blocked[r])
            total = 0
            while free:
                bit = free & -free
                free ^= bit
                total += go(r + 1, cols | bit, (d1 | bit) << 1 & full, (d2 | bit) >> 1)
            return total

        return go(0, 0, 0, 0)
