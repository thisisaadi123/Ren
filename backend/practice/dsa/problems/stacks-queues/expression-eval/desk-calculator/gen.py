LIM = 10**9
def make(rng, n, hi=1000, shape="random", space=0.0):
    toks, total, length = [], None, 0
    tail = shape == "tail-products"
    while length < n:
        if tail and total is not None and length >= n // 2:
            t, v = ["2"], 2
            while length + 2 * len(t) < n:
                if rng.random() < 0.5:
                    t += ["*", "1"]
                else:
                    t += ["/", "1"]
        else:
            v = rng.randint(0, hi)
            t = [str(v)]
            chain = 0 if shape in ("sums", "tail-products") else rng.randint(0, 3)
            for _ in range(chain):
                m = rng.randint(0, hi)
                if rng.random() < 0.5 and v * m <= LIM:
                    t += ["*", str(m)]
                    v *= m
                else:
                    d = rng.randint(1, hi)
                    t += ["/", str(d)]
                    v //= d
        if total is None:
            total = v
            toks += t
        else:
            sign = rng.choice("+-")
            if abs(total + (v if sign == "+" else -v)) > LIM:
                sign = "-" if sign == "+" else "+"
            total += v if sign == "+" else -v
            toks += [sign] + t
        length += sum(len(x) for x in t) + 1
    out = []
    for i, x in enumerate(toks):
        if i and rng.random() < space:
            out.append(" ")
        out.append(x)
    return "".join(out)
def small(rng):
    return {"expr": make(rng, rng.randint(1, 16), hi=rng.choice([9, 30]), space=0.2)}
def build(rng, n, hi=1000, shape="random", space=0.0):
    return {"expr": make(rng, int(n), int(hi), shape, float(space))}
