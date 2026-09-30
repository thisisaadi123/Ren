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
    return {"panels": [rng.randint(1, 5) for _ in range(rng.randint(1, 9))]}
def build(rng, n, shape="random", hi=10**9):
    return {"panels": arr(rng, n, 1, int(hi), shape)}
