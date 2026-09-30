def small(rng):
    return {"first": sorted(rng.randint(0, 6) for _ in range(rng.randint(0, 5))),
            "second": sorted(rng.randint(0, 6) for _ in range(rng.randint(0, 5)))}


def build(rng, n, m, span=10**6, shape="random"):
    if shape == "disjoint":  # every first value below every second value
        return {"first": sorted(rng.randint(-span, -1) for _ in range(n)),
                "second": sorted(rng.randint(0, span) for _ in range(m))}
    if shape == "interleave":
        return {"first": list(range(0, 2 * n, 2)), "second": list(range(1, 2 * m, 2))}
    return {"first": sorted(rng.randint(-span, span) for _ in range(n)),
            "second": sorted(rng.randint(-span, span) for _ in range(m))}
