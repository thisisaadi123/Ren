def build(rng, n, m, meet=1, at=-1):
    # A line that never joins needs at least one stop of its own.
    vals = rng.sample(range(1, 10**5 + 1), n + max(m, 1))
    a, own = vals[:n], vals[n:n + m]
    if not meet:
        return {"headA": a, "headB": vals[n:]}
    j = at if 0 <= at < n else rng.randrange(n)
    return {"headA": a, "headB": {"values": own, "join_at": j}}


def small(rng):
    n = rng.randint(1, 6)
    return build(rng, n, rng.randint(0 if rng.random() < 0.8 else 1, 4), 1 if rng.random() < 0.75 else 0)
