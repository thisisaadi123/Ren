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


def naive_steps(g, cap):
    # how many (cell, digit) tries a plain row-by-row search makes
    rows = [0] * 9; cols = [0] * 9; boxes = [0] * 9
    for r in range(9):
        for c in range(9):
            if g[r][c]:
                b = 1 << g[r][c]
                rows[r] |= b; cols[c] |= b; boxes[r // 3 * 3 + c // 3] |= b
    cells = [(r, c, r // 3 * 3 + c // 3) for r in range(9) for c in range(9) if not g[r][c]]
    steps = 0

    def go(i):
        nonlocal steps
        if i == len(cells):
            return True
        r, c, k = cells[i]
        for v in range(1, 10):
            steps += 1
            if steps > cap:
                return True
            b = 1 << v
            if not (rows[r] & b or cols[c] & b or boxes[k] & b):
                rows[r] |= b; cols[c] |= b; boxes[k] |= b
                if go(i + 1):
                    return True
                rows[r] ^= b; cols[c] ^= b; boxes[k] ^= b
        return False

    go(0)
    return steps


def carve(rng, g, keep=17):
    cells = [(r, c) for r in range(9) for c in range(9)]
    rng.shuffle(cells)
    left = 81
    for r, c in cells:
        if left <= keep:
            break
        v = g[r][c]
        g[r][c] = 0
        if count(g) != 1:
            g[r][c] = v
        else:
            left -= 1
    return g


def anti(g, sol):
    # relabel digits so the first empty cells (row by row) hold 9, 8, 7, ...
    mp, nxt = {}, 9
    for r in range(9):
        for c in range(9):
            if not g[r][c] and sol[r][c] not in mp:
                mp[sol[r][c]] = nxt
                nxt -= 1
    for d in range(1, 10):
        if d not in mp:
            mp[d] = nxt
            nxt -= 1
    return [[mp[v] if v else 0 for v in row] for row in g]


def to_board(g):
    return [[str(v) if v else "." for v in row] for row in g]


def small(rng):
    while True:
        g = solved(rng)
        k = rng.randint(1, 22)
        cells = rng.sample([(r, c) for r in range(9) for c in range(9)], k)
        for r, c in cells:
            g[r][c] = 0
        if count(g) == 1:
            return {"board": to_board(g)}


def build(rng, shape="minimal", keep=17, tries=4):
    if shape == "anti":
        best, best_steps = None, -1
        for _ in range(tries):
            sol = solved(rng)
            g = carve(rng, [row[:] for row in sol])
            a = anti(g, sol)
            s = naive_steps(a, 3_000_000)
            if s > best_steps:
                best, best_steps = a, s
        return {"board": to_board(best)}
    g = carve(rng, solved(rng), keep)
    return {"board": to_board(g)}
