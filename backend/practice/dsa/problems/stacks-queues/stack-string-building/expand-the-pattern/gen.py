def make(rng, budget, depth, alpha, kmax):
    """A random pattern whose expansion is at most `budget` letters, and its expanded length."""
    parts, size = [], 0
    for _ in range(rng.randint(1, 3)):
        if depth > 0 and rng.random() < 0.6 and budget - size >= 2:
            k = rng.randint(1, min(kmax, budget - size))
            inner, n = make(rng, (budget - size) // k, depth - 1, alpha, kmax)
            if n * k + size <= budget and n:
                parts.append("%d[%s]" % (k, inner))
                size += n * k
                continue
        w = "".join(rng.choice(alpha) for _ in range(rng.randint(1, 3)))
        if size + len(w) <= budget:
            parts.append(w)
            size += len(w)
    if not parts:
        parts, size = [alpha[0]], 1
    return "".join(parts), size


def build(rng, budget, depth=3, alpha=3, kmax=9, shape="random"):
    letters = "abcdefghijklmnopqrstuvwxyz"[:alpha]
    if shape == "deep":
        # Many nested 2[...] layers around one letter: 2^16 letters.
        return {"pattern": "2[" * 16 + "a" + "]" * 16}
    if shape == "wide":
        return {"pattern": "300[" + "abc" + "]" + "100[" + letters + "]"}
    if shape == "flat":
        return {"pattern": "".join(rng.choice(letters) for _ in range(min(budget, 3000)))}
    p, _ = make(rng, budget, depth, letters, kmax)
    return {"pattern": p[:3000] if len(p) <= 3000 else make(rng, budget // 4, depth, letters, kmax)[0]}


def small(rng):
    return build(rng, rng.randint(1, 12), rng.randint(0, 3), 2, rng.choice((3, 12)))
