def build(rng, n=14, cap=100, lo=10, hi=60):
    cap = rng.randint(max(1, cap // 2), cap)
    lo_w = max(1, cap * lo // 100)
    hi_w = max(lo_w, min(cap, cap * hi // 100))
    return {"boxes": [rng.randint(lo_w, hi_w) for _ in range(n)], "capacity": cap}


def small(rng):
    return build(rng, rng.randint(1, 7), rng.randint(1, 20), 1, 100)
