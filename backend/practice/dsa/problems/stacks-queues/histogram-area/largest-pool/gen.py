def arr(rng, n, lo, hi, shape):
    if shape == "inc":
        return sorted(rng.randint(lo, hi) for _ in range(n))
    if shape == "dec":
        return sorted((rng.randint(lo, hi) for _ in range(n)), reverse=True)
    if shape == "equal":
        return [rng.randint(lo, hi)] * n
    if shape == "few":
        vals = [rng.randint(lo, hi) for _ in range(3)]
        return [rng.choice(vals) for _ in range(n)]
    if shape == "valley":
        return arr(rng, n // 2, lo, hi, "dec") + arr(rng, n - n // 2, lo, hi, "inc")
    if shape == "peak":
        return arr(rng, n // 2, lo, hi, "inc") + arr(rng, n - n // 2, lo, hi, "dec")
    if shape == "saw":
        return [hi if i % 2 == 0 else rng.randint(lo, hi) for i in range(n)]
    return [rng.randint(lo, hi) for _ in range(n)]

def small(rng):
    return {"walls": [rng.randint(0, 5) for _ in range(rng.randint(1, 10))]}
def build(rng, n, shape="random", hi=10**9):
    hi = int(hi)
    if shape == "basins":
        a = []
        while len(a) < n:
            k = rng.randint(2, 50)
            a += [hi] + [rng.randint(0, hi // 2) for _ in range(k)]
        return {"walls": a[:n - 1] + [hi]}
    if shape == "equal-walls":
        return {"walls": [hi if i % 3 == 0 else rng.randint(0, hi - 1) for i in range(n)]}
    return {"walls": arr(rng, n, 0, hi, shape)}
