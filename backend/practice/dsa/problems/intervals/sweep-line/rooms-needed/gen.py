def rand_intervals(rng, n, span=1000, maxlen=50, zero=False):
    out = []
    for _ in range(n):
        s = rng.randint(0, max(0, min(span, 10**9 - maxlen)))
        e = s + rng.randint(0 if zero else 1, maxlen)
        out.append([s, e])
    return out


def disjoint(rng, n, span=1000, touch=False):
    """n sorted, non-overlapping intervals (touching allowed if touch)."""
    pts = sorted(rng.sample(range(0, max(span, 2 * n + 2)), 2 * n))
    out = [[pts[2 * i], pts[2 * i + 1]] for i in range(n)]
    if touch:
        for i in range(1, n):
            if rng.random() < 0.3 and out[i - 1][1] < out[i][1]:
                out[i][0] = out[i - 1][1]
    return out


def build(rng, n, span=1000, maxlen=50, touch=0):
    m = rand_intervals(rng, n, span, maxlen)
    if touch:
        for i in range(1, n):
            if rng.random() < 0.4:
                m[i] = [m[i - 1][1], m[i - 1][1] + rng.randint(1, maxlen)]
    return {"meetings": m}


def small(rng):
    return build(rng, rng.randint(1, 6), 20, 6, rng.choice((0, 1)))
