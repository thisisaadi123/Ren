def build(rng, n, depot=10**6, top=10**6, shape="random"):
    depot = max(depot, n)
    pos = rng.sample(range(depot), n)
    if shape == "ties":
        # Many trucks arrive at exactly the same moment.
        sp = []
        for p in pos:
            d = depot - p
            divisors = [x for x in (1, 2, 3, 4, 5, 6, 8, 10, 12) if d % x == 0]
            sp.append(rng.choice(divisors))
        return {"depot": depot, "position": pos, "speed": sp}
    if shape == "chase":
        # Faster trucks behind: everyone merges.
        order = sorted(pos)
        sp = {p: n - i for i, p in enumerate(order)}
        return {"depot": depot, "position": pos, "speed": [min(top, sp[p]) for p in pos]}
    return {"depot": depot, "position": pos, "speed": [rng.randint(1, top) for _ in pos]}


def small(rng):
    n = rng.randint(1, 6)
    return build(rng, n, rng.randint(n, 15), rng.choice((3, 10)), rng.choice(("random", "ties")))
