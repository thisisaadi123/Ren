def balanced(rng, n, p=0.5):
    out, st, opens = [], 0, n // 2
    while len(out) < n:
        if opens and (not st or rng.random() < p):
            out.append("("); st += 1; opens -= 1
        else:
            out.append(")"); st -= 1
    return "".join(out)
def small(rng):
    n = rng.randint(1, 14)
    if rng.random() < 0.3:
        return {"s": "(" * rng.randint(0, 3) + balanced(rng, 2 * rng.randint(1, 4)) + ")" * rng.randint(0, 3)}
    return {"s": "".join(rng.choice("()") for _ in range(n))}
def build(rng, n, shape="random", p=0.5):
    if shape == "opens":
        s = "(" * n
    elif shape == "flat":
        s = "()" * (n // 2) + "(" * (n % 2)
    elif shape == "extra-open":
        s = "(" + balanced(rng, n - 1 - (n - 1) % 2)
    elif shape == "pieces":
        parts, total = [], 0
        while total < n:
            k = rng.randint(1, max(1, n // 20)) * 2
            k = min(k, n - total)
            if k < 2:
                parts.append(")"); total += 1
                continue
            parts.append(balanced(rng, k - k % 2))
            parts.append(rng.choice(")("))
            total += k - k % 2 + 1
        s = "".join(parts)[:n]
    else:
        s = "".join("(" if rng.random() < float(p) else ")" for _ in range(n))
    return {"s": s}
