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
    return {"values": [rng.randint(-4, 4) for _ in range(rng.randint(1, 8))]}
def build(rng, n, shape="random", lo=-10**9, hi=10**9):
    lo, hi = int(lo), int(hi)
    if shape == "late":
        a = arr(rng, n - 3, lo + 10, hi, "inc")
        a += [lo + 1, lo + 5, lo + 3]
        return {"values": a}
    if shape == "zigzag":
        a = []
        for i in range(n):
            a.append(-i if i % 2 else i)
        return {"values": [max(lo, min(hi, x)) for x in a]}
    return {"values": arr(rng, n, lo, hi, shape)}
