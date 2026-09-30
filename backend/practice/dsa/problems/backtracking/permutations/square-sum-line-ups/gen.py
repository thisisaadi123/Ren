import math
def chain(rng, n, lo=0, hi=60, step=4):
    a = [rng.randint(lo, hi)]
    while len(a) < n:
        r = math.isqrt(a[-1])
        s = r + rng.randint(1, step)
        a.append(s * s - a[-1])
    return a
def small(rng):
    n = rng.randint(1, 7)
    shape = rng.choice(["chain", "tiny", "pair"])
    if shape == "chain":
        a = chain(rng, n, 0, 20, 3)
    elif shape == "pair":
        x, y = rng.choice([(2, 98), (1, 3), (0, 1), (0, 0), (8, 8), (1, 8), (6, 19)])
        a = [rng.choice([x, y]) for _ in range(n)]
    else:
        a = [rng.randint(0, 17) for _ in range(n)]
    rng.shuffle(a)
    return {"nums": a}
def build(rng, n, shape="chain", hi=60, step=4):
    if shape == "chain":
        a = chain(rng, n, 0, hi, step)
    elif shape == "bigchain":
        a = chain(rng, n, 10**8, 3 * 10**8, 50)
        if max(a) > 10**9:
            a = chain(rng, n, 0, 1000, 3)
    elif shape == "zigzag":          # two values that pair, repeated
        x, y = rng.choice([(1, 3), (2, 7), (5, 11), (6, 10), (12, 13), (40, 41)])
        a = [x if i % 2 == 0 else y for i in range(n)]
    elif shape == "doubles":         # values whose doubles are squares, pairing with each other
        a = [rng.choice([2, 98, 578]) for _ in range(n)]
    elif shape == "triangle":        # 6 + 19, 6 + 30, 19 + 30 are all squares
        a = [rng.choice([6, 19, 30]) for _ in range(n)]
    elif shape == "zeros":
        a = [0] * (n - 2) + [1, 4]
    else:
        a = [rng.randint(0, hi) for _ in range(n)]
    rng.shuffle(a)
    return {"nums": a}
