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


def build(rng, n, m=0, span=10000, clash=50):
    m = m or n
    if rng.randrange(100) >= clash:
        # Deal one sorted run of disjoint slots out to the two calendars: they can't clash.
        run = disjoint(rng, n + m, span)
        flags = [True] * n + [False] * m
        rng.shuffle(flags)
        a = [x for x, f in zip(run, flags) if f]
        b = [x for x, f in zip(run, flags) if not f]
        return {"a": a or [[0, 1]], "b": b or [[10**9 - 1, 10**9]]}
    a = [x for x in disjoint(rng, n, span, touch=True) if x[0] < x[1]] or [[0, 1]]
    b = [x for x in disjoint(rng, m, span, touch=True) if x[0] < x[1]] or [[2, 3]]
    return {"a": a, "b": b}


def small(rng):
    return build(rng, rng.randint(1, 4), rng.randint(1, 4), 25)
