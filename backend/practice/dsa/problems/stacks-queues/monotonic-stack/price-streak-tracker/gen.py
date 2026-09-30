def arr(rng, n, lo, hi, shape):
    if shape == "inc":
        a = sorted(rng.randint(lo, hi) for _ in range(n))
        return [lo + i if lo + i <= hi else hi for i in range(n)] if hi - lo >= n else a
    if shape == "dec":
        a = arr(rng, n, lo, hi, "inc")
        return a[::-1]
    if shape == "equal":
        return [rng.randint(lo, hi)] * n
    if shape == "few":
        vals = [rng.randint(lo, hi) for _ in range(3)]
        return [rng.choice(vals) for _ in range(n)]
    if shape == "valley":
        a = arr(rng, n // 2, lo, hi, "dec")
        return a + arr(rng, n - n // 2, lo, hi, "inc")
    if shape == "peak":
        a = arr(rng, n // 2, lo, hi, "inc")
        return a + arr(rng, n - n // 2, lo, hi, "dec")
    return [rng.randint(lo, hi) for _ in range(n)]

def small(rng):
    a = [rng.randint(1, 6) for _ in range(rng.randint(1, 10))]
    return {"calls": [["PriceStreak"]] + [["record", p] for p in a]}
def build(rng, n, shape="random", hi=10**9):
    a = arr(rng, n, 1, int(hi), shape)
    return {"calls": [["PriceStreak"]] + [["record", p] for p in a]}
