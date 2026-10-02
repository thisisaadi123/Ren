def vocab(rng, count, lo, hi, alpha):
    return ["".join(rng.choice(alpha) for _ in range(rng.randint(lo, hi))) for _ in range(count)]


def build(rng, n, alpha="abc", lo=1, hi=5, add=40):
    pool = vocab(rng, max(3, n // 3), lo, hi, alpha)
    calls = [["WildcardDictionary"]]
    for _ in range(n):
        w = rng.choice(pool)
        if rng.randrange(100) < add:
            calls.append(["addWord", w])
        else:
            p = list(w)
            for i in rng.sample(range(len(p)), min(len(p), rng.randint(0, 3))):
                p[i] = "."
            if rng.random() < 0.15:
                p = p[:-1] or ["."]
            calls.append(["search", "".join(p)])
    return {"calls": calls}


def small(rng):
    return build(rng, rng.randint(1, 10), "ab", 1, 3)
