class Solution:
    def fillGrid(self, board):
        FULL = 0x3FE
        rows = [0] * 9; cols = [0] * 9; boxes = [0] * 9
        empty = []
        g = [row[:] for row in board]
        for r in range(9):
            for c in range(9):
                if g[r][c] == ".":
                    empty.append((r, c, r // 3 * 3 + c // 3))
                else:
                    b = 1 << int(g[r][c])
                    rows[r] |= b; cols[c] |= b; boxes[r // 3 * 3 + c // 3] |= b

        def go():
            if not empty:
                return True
            bc, bi, best = 10, -1, 0
            for i, (r, c, k) in enumerate(empty):
                m = FULL & ~(rows[r] | cols[c] | boxes[k])
                cnt = bin(m).count("1")
                if cnt < bc:
                    bc, bi, best = cnt, i, m
                    if cnt <= 1:
                        break
            if bc == 0:
                return False
            r, c, k = empty[bi]
            empty[bi] = empty[-1]
            empty.pop()
            m = best
            while m:
                bit = m & -m
                m ^= bit
                rows[r] |= bit; cols[c] |= bit; boxes[k] |= bit
                if go():
                    g[r][c] = str(bit.bit_length() - 1)
                    return True
                rows[r] ^= bit; cols[c] ^= bit; boxes[k] ^= bit
            empty.append((r, c, k))
            empty[bi], empty[-1] = empty[-1], empty[bi]
            return False

        go()
        return g
