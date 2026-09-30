FULL = 0x3FE


def solved(rng):
    def shuf(x):
        x = list(x)
        rng.shuffle(x)
        return x
    rows = [b * 3 + r for b in shuf(range(3)) for r in shuf(range(3))]
    cols = [s * 3 + c for s in shuf(range(3)) for c in shuf(range(3))]
    nums = shuf(range(1, 10))
    return [[nums[(3 * (r % 3) + r // 3 + c) % 9] for c in cols] for r in rows]


def count(grid, limit=2):
    rows = [0] * 9; cols = [0] * 9; boxes = [0] * 9; empty = []
    for r in range(9):
        for c in range(9):
            v = grid[r][c]
            if v:
                b = 1 << v
                k = r // 3 * 3 + c // 3
                if rows[r] & b or cols[c] & b or boxes[k] & b:
                    return 0
                rows[r] |= b; cols[c] |= b; boxes[k] |= b
            else:
                empty.append((r, c, r // 3 * 3 + c // 3))
    found = 0

    def go():
        nonlocal found
        if not empty:
            found += 1
            return
        bc, bi, best = 10, -1, 0
        for i, (r, c, b) in enumerate(empty):
            m = FULL & ~(rows[r] | cols[c] | boxes[b])
            k = bin(m).count("1")
            if k < bc:
                bc, bi, best = k, i, m
                if k <= 1:
                    break
        if bc == 0:
            return
        r, c, b = empty[bi]
        empty[bi] = empty[-1]
        empty.pop()
        m = best
        while m and found < limit:
            bit = m & -m
            m ^= bit
            rows[r] |= bit; cols[c] |= bit; boxes[b] |= bit
            go()
            rows[r] ^= bit; cols[c] ^= bit; boxes[b] ^= bit
        empty.append((r, c, b))
        empty[bi], empty[-1] = empty[-1], empty[bi]

    go()
    return found


def validate(board):
    assert isinstance(board, list) and len(board) == 9, "board has 9 rows"
    g = []
    for row in board:
        assert isinstance(row, list) and len(row) == 9, "each row has 9 cells"
        for ch in row:
            assert isinstance(ch, str) and len(ch) == 1 and ch in ".123456789", "cells are '1'-'9' or '.'"
        g.append([0 if ch == "." else int(ch) for ch in row])
    n = count(g, 2)
    assert n != 0, "the clues can't be completed into a valid grid"
    assert n == 1, "the puzzle has exactly one solution"
