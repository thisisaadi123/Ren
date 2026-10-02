def build(rng, n, m, k=0, hi=10**9):
    a = sorted(rng.randint(-hi, hi) for _ in range(n))
    b = sorted(rng.randint(-hi, hi) for _ in range(m))
    cap = min(n * m, 10**4)
    return {"a": a, "b": b, "k": min(k, cap) if k else rng.randint(1, cap)}


def small(rng):
    return build(rng, rng.randint(1, 5), rng.randint(1, 5), 0, rng.choice((3, 10)))
