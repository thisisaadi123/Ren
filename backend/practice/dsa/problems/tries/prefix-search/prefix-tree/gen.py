def vocab(rng, count, lo, hi, alpha):
    return ["".join(rng.choice(alpha) for _ in range(rng.randint(lo, hi))) for _ in range(count)]


def build(rng, n, alpha="abc", lo=1, hi=6, insert=40):
    pool = vocab(rng, max(3, n // 3), lo, hi, alpha)
    calls = [["PrefixTree"]]
    for _ in range(n):
        r = rng.randrange(100)
        w = rng.choice(pool)
        if r < insert:
            calls.append(["insert", w])
        elif r < 70:
            calls.append(["search", w if rng.random() < 0.7 else w[:rng.randint(1, len(w))]])
        else:
            calls.append(["startsWith", w[:rng.randint(1, len(w))] if rng.random() < 0.8 or len(w) >= 50 else w + rng.choice(alpha)])
    return {"calls": calls}


def small(rng):
    return build(rng, rng.randint(1, 10), "ab", 1, 3)
