def build(rng, n, veg=50, tray_veg=-1, shape="random"):
    p = [0 if rng.random() < veg / 100 else 1 for _ in range(n)]
    tv = veg if tray_veg < 0 else tray_veg
    t = [0 if rng.random() < tv / 100 else 1 for _ in range(n)]
    if shape == "match":
        t = sorted(p)
        rng.shuffle(t)
    return {"prefers": p, "trays": t}


def small(rng):
    return build(rng, rng.randint(1, 7), rng.choice((30, 50, 70)), -1, rng.choice(("random", "match")))
