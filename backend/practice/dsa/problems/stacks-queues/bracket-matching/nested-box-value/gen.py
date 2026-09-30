def balanced(rng, n, p=0.5):
    out, st, opens = [], 0, n // 2
    while len(out) < n:
        if opens and (not st or rng.random() < p):
            out.append("("); st += 1; opens -= 1
        else:
            out.append(")"); st -= 1
    return "".join(out)
def small(rng):
    return {"s": balanced(rng, 2 * rng.randint(1, 7))}
def build(rng, n, shape="random"):
    n -= n % 2
    if shape == "nested":
        s = "(" * (n // 2) + ")" * (n // 2)
    elif shape == "flat":
        s = "()" * (n // 2)
    elif shape == "deep":
        s = balanced(rng, n, 0.85)
    elif shape == "deep-chunks":
        k = 70
        s = ("(" * k + ")" * k) * (n // (2 * k))
        s += "()" * ((n - len(s)) // 2)
    else:
        s = balanced(rng, n)
    return {"s": s}
