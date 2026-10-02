def grid(rng, m, n, alpha):
    return [[rng.choice(alpha) for _ in range(n)] for _ in range(m)]


def build(rng, m, n, k, alpha="ab", traced=1):
    g = grid(rng, m, n, alpha)
    if traced:
        r, c = rng.randrange(m), rng.randrange(n)
        seen, w = {(r, c)}, [g[r][c]]
        while len(w) < k:
            opts = [(r + dr, c + dc) for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)) if 0 <= r + dr < m and 0 <= c + dc < n and (r + dr, c + dc) not in seen]
            if not opts:
                break
            r, c = rng.choice(opts)
            seen.add((r, c))
            w.append(g[r][c])
        word = "".join(w)
    else:
        word = "".join(rng.choice(alpha) for _ in range(k))
    return {"board": g, "word": word}


def small(rng):
    return build(rng, rng.randint(1, 3), rng.randint(1, 3), rng.randint(1, 5), "ab", rng.choice((0, 1)))
