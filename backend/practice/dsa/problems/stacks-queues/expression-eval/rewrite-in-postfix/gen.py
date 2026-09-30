import string
PREC = {"+": 1, "-": 1, "*": 2, "/": 2, "^": 3}
def rope_join(r):
    out, st = [], [r]
    while st:
        x = st.pop()
        if isinstance(x, str):
            out.append(x)
        else:
            st.extend(reversed(x))
    return "".join(out)
def tree(rng, leaves, ops, paren):
    # combine random pieces; each piece is (rope, precedence of its top operator, 9 for a letter)
    items = [(rng.choice(string.ascii_lowercase), 9) for _ in range(leaves)]
    while len(items) > 1:
        i = rng.randrange(len(items) - 1)
        (a, pa), (b, pb) = items[i], items[i + 1]
        op = rng.choice(ops)
        p = PREC[op]
        left_needs = pa < p or (pa == p and op == "^")
        right_needs = pb < p or (pb == p and op != "^")
        if left_needs or rng.random() < paren:
            a, pa = ("(", a, ")"), 9
        if right_needs or rng.random() < paren:
            b, pb = ("(", b, ")"), 9
        items[i:i + 2] = [((a, op, b), p)]
    return rope_join(items[0][0])
def small(rng):
    return {"expr": tree(rng, rng.randint(1, 6), "+-*/^", 0.15)}
def build(rng, n, shape="random", ops="+-*/^", paren=0.1):
    letters = lambda: rng.choice(string.ascii_lowercase)
    if shape == "chain":
        parts = [letters()]
        while len(parts) < n - 1:
            parts += [rng.choice(ops), letters()]
        return {"expr": "".join(parts)}
    if shape == "deep":
        r, size = letters(), 1
        while size + 4 <= n:
            r = ("(", r, rng.choice(ops), letters(), ")")
            size += 4
        return {"expr": rope_join(r)}
    if shape == "power-chain":
        parts = [letters()]
        while len(parts) < n - 1:
            parts += ["^", letters()]
        return {"expr": "".join(parts)}
    leaves = max(1, int(n) // 3)
    while True:
        e = tree(rng, leaves, ops, float(paren))
        if len(e) <= n:
            return {"expr": e}
        leaves = int(leaves * 0.9)
