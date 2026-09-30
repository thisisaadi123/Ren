LIM = 10**9
PREC = {"+": 1, "-": 1, "*": 2, "/": 2}
def apply(a, b, op):
    if op == "+":
        return a + b
    if op == "-":
        return a - b
    if op == "*":
        return a * b
    q = abs(a) // abs(b)
    return q if (a < 0) == (b < 0) else -q
def pick(rng, va, vb, ops):
    order = list(ops)
    rng.shuffle(order)
    for op in order + ["+", "-", "/"]:
        if op == "/" and vb == 0:
            continue
        r = apply(va, vb, op)
        if abs(r) <= LIM:
            return op, r
def neg(item):
    r, v, p = item
    inner = r if p >= 2 else ("(", r, ")")
    return (("(", "-", inner, ")"), -v, 9)
def flatten(r):
    out, st = [], [r]
    while st:
        x = st.pop()
        if isinstance(x, str):
            out.append(x)
        else:
            st.extend(reversed(x))
    return out
def render(rng, root, space, lead_neg):
    r, v, p = root
    if lead_neg:
        r = ("-", r if p >= 2 else ("(", r, ")"))
    toks = flatten(r)
    out = []
    for i, x in enumerate(toks):
        if i and rng.random() < space:
            out.append(" ")
        out.append(x)
    if rng.random() < space:
        out = [" "] + out + [" "]
    return "".join(out)
def tree(rng, leaves, hi, ops, paren, pneg):
    items = []
    for _ in range(leaves):
        v = rng.randint(0, hi)
        it = (str(v), v, 9)
        items.append(neg(it) if rng.random() < pneg else it)
    while len(items) > 1:
        i = rng.randrange(len(items) - 1)
        (ra, va, pa), (rb, vb, pb) = items[i], items[i + 1]
        op, v = pick(rng, va, vb, ops)
        p = PREC[op]
        if pa < p or rng.random() < paren:
            ra = ("(", ra, ")")
        if pb <= p or rng.random() < paren:
            rb = ("(", rb, ")")
        it = ((ra, op, rb), v, p)
        items[i:i + 2] = [neg(it) if rng.random() < pneg else it]
    return items[0]
def deep(rng, n, hi, ops):
    v = rng.randint(0, hi)
    r, size = str(v), len(str(v))
    while size + 6 < n:
        b = rng.randint(1, hi)
        op, v = pick(rng, v, b, ops)
        r = ("(", r, op, str(b), ")")
        size += 3 + len(str(b))
    return (r, v, 9)
def small(rng):
    root = tree(rng, rng.randint(1, 5), 9, "+-*/", 0.2, 0.15)
    return {"expr": render(rng, root, 0.2, rng.random() < 0.15)}
def build(rng, n, hi=1000, shape="random", ops="+-*/", paren=0.1, pneg=0.05, space=0.0):
    n, hi = int(n), int(hi)
    if shape == "deep":
        return {"expr": render(rng, deep(rng, n, hi, ops), 0.0, False)}
    leaves = max(1, n // (len(str(hi)) + 2))
    while True:
        root = tree(rng, leaves, hi, ops, float(paren), float(pneg))
        e = render(rng, root, float(space), rng.random() < 0.3)
        if len(e) <= n:
            return {"expr": e}
        leaves = int(leaves * 0.85)
