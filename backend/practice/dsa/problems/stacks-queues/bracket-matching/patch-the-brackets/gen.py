def balanced(rng, n, kinds="()"):
    out, st, opens = [], [], n // 2
    while len(out) < n:
        if opens and (not st or rng.random() < 0.5):
            k = rng.randrange(len(kinds) // 2)
            out.append(kinds[2 * k]); st.append(kinds[2 * k + 1]); opens -= 1
        else:
            out.append(st.pop())
    return "".join(out)

def small(rng):
    return {"s": "".join(rng.choice("()") for _ in range(rng.randint(1, 14)))}
def build(rng, n, shape="random"):
    if shape == "nested":
        s = "(" * (n // 2) + ")" * (n - n // 2)
    elif shape == "opens":
        s = "(" * n
    elif shape == "flipped":
        s = ")" * (n // 2) + "(" * (n - n // 2)
    elif shape == "near":
        s = list(balanced(rng, n - n % 2))
        for _ in range(10):
            s[rng.randrange(len(s))] = rng.choice("()")
        s = "".join(s)
    else:
        s = "".join(rng.choice("()") for _ in range(n))
    return {"s": s}
