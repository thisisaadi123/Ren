def vocab(rng, count, lo, hi, alpha):
    return ["".join(rng.choice(alpha) for _ in range(rng.randint(lo, hi))) for _ in range(count)]


def board(rng, m, n, alpha):
    return ["".join(rng.choice(alpha) for _ in range(n)) for _ in range(m)]


def traced(rng, rows, length, diag=False, straight=False):
    """A word read off the board along a random path (or a straight line)."""
    m, n = len(rows), len(rows[0])
    r, c = rng.randrange(m), rng.randrange(n)
    dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)] + ([(1, 1), (1, -1), (-1, 1), (-1, -1)] if diag else [])
    if straight:
        dr, dc = rng.choice(dirs)
        out = []
        while 0 <= r < m and 0 <= c < n and len(out) < length:
            out.append(rows[r][c])
            r, c = r + dr, c + dc
        return "".join(out)
    seen, out = {(r, c)}, [rows[r][c]]
    while len(out) < length:
        opts = [(r + dr, c + dc) for dr, dc in dirs if 0 <= r + dr < m and 0 <= c + dc < n and (r + dr, c + dc) not in seen]
        if not opts:
            break
        r, c = rng.choice(opts)
        seen.add((r, c))
        out.append(rows[r][c])
    return "".join(out)


def build(rng, m, n, count, alpha="abcd", hit=50, hi=8):
    rows = board(rng, m, n, alpha)
    words = []
    for _ in range(count):
        if rng.randrange(100) < hit:
            words.append(traced(rng, rows, rng.randint(1, hi), diag=True, straight=True))
        elif rng.random() < 0.5:
            words.append(traced(rng, rows, rng.randint(2, hi)))  # bends: usually not straight
        else:
            words.append("".join(rng.choice(alpha) for _ in range(rng.randint(1, hi))))
    return {"board": rows, "words": words}


def small(rng):
    return build(rng, rng.randint(1, 4), rng.randint(1, 4), rng.randint(1, 5), "ab", 50, 4)
