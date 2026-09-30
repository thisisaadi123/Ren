def make(rng, n, shape, lo, hi):
    ks = sorted(rng.sample(range(lo, hi + 1), n))
    if shape == "asc":
        return ks
    if shape == "desc":
        return ks[::-1]
    if shape == "zigzag":
        out, a, b = [], 0, n - 1
        while a <= b:
            out.append(ks[a]); a += 1
            if a <= b:
                out.append(ks[b]); b -= 1
        return out
    if shape == "inward":
        # the middle key first, then keys alternately just below and just above: two long chains
        m = n // 2
        out = [ks[m]]
        a, b = m - 1, m + 1
        while a >= 0 or b < n:
            if a >= 0:
                out.append(ks[a]); a -= 1
            if b < n:
                out.append(ks[b]); b += 1
        return out
    if shape == "balanced":
        out, stack = [], [(0, n - 1)]
        while stack:
            a, b = stack.pop(0) if len(stack) < 4 else stack.pop()
            if a > b:
                continue
            m = (a + b) // 2
            out.append(ks[m])
            stack.append((a, m - 1))
            stack.append((m + 1, b))
        return out
    if shape == "nearly":
        out = ks[:]
        for _ in range(max(1, n // 50)):
            i = rng.randrange(n)
            j = min(n - 1, i + rng.randint(1, 5))
            out[i], out[j] = out[j], out[i]
        return out
    rng.shuffle(ks)
    return ks


def small(rng):
    n = rng.randint(1, 9)
    return {"keys": make(rng, n, rng.choice(["random", "random", "asc", "desc", "zigzag", "inward", "balanced"]), -15, 15)}


def build(rng, n, shape="random", lo=-10**9, hi=10**9):
    return {"keys": make(rng, n, shape, lo, hi)}
