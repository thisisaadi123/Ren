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
    n = rng.randint(1, 12)
    if rng.random() < 0.5:
        s = list(balanced(rng, n - n % 2 or 2, "()[]{}"))
        if rng.random() < 0.6:
            s[rng.randrange(len(s))] = rng.choice("()[]{}")
        return {"s": "".join(s)}
    return {"s": "".join(rng.choice("()[]{}") for _ in range(n))}
def build(rng, n, shape="balanced"):
    if shape == "nested":
        k = n // 2
        opens = [rng.choice("([{") for _ in range(k)]
        close = {"(": ")", "[": "]", "{": "}"}
        s = "".join(opens) + "".join(close[c] for c in reversed(opens))
    elif shape == "broken-end":
        s = balanced(rng, n - 1 - (n - 1) % 2, "()[]{}")
        s = s[:-1] + {")": "]", "]": "}", "}": ")"}[s[-1]]
    elif shape == "random":
        s = "".join(rng.choice("()[]{}") for _ in range(n))
    else:
        s = balanced(rng, n - n % 2, "()[]{}")
    return {"s": s}
