def make(rng, n, m, shape):
    colours = [chr(97 + i) for i in range(m)]
    s = [rng.choice(colours) for _ in range(n)]
    if shape == "perm":
        k = min(n, m)
        for i, c in enumerate(rng.sample(colours, k)):
            s[rng.randrange(n)] = c
        present = sorted(set(s))
        perm = present[:]
        rng.shuffle(perm)
        f = dict(zip(present, perm))
    else:
        f = {c: rng.choice(colours) for c in colours}
    t = [f[c] for c in s]
    if shape == "same":
        t = s[:]
    elif shape == "random":
        t = [rng.choice(colours) for _ in range(n)]
    elif shape == "broken" and m > 1:
        i = rng.randrange(n)
        t[i] = rng.choice([c for c in colours if c != t[i]])
    return {"s": "".join(s), "t": "".join(t), "m": m}
def small(rng):
    m = rng.randint(1, 4)
    n = rng.randint(1, 6 if m <= 3 else 4)
    return make(rng, n, m, rng.choice(["func", "func", "perm", "perm", "same", "random", "broken"]))
def build(rng, n, m, shape="func"):
    return make(rng, n, m, shape)
