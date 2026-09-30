LIM = 10**9
def apply(a, b, op):
    if op == "+":
        return a + b
    if op == "-":
        return a - b
    if op == "*":
        return a * b
    q = abs(a) // abs(b)
    return q if (a < 0) == (b < 0) else -q
def make(rng, nums, shape="random", lo=-200, hi=200, ops="+-*/"):
    toks, st = [], []
    def push():
        v = rng.randint(lo, hi)
        toks.append(str(v)); st.append(v)
    def reduce():
        b, a = st.pop(), st.pop()
        order = list(ops); rng.shuffle(order)
        order += [o for o in "+-/" if o not in order]
        for op in order:
            if op == "/" and b == 0:
                continue
            r = apply(a, b, op)
            if abs(r) <= LIM:
                break
        toks.append(op); st.append(r)
    if shape == "tail-ops":
        for _ in range(nums):
            push()
        while len(st) > 1:
            reduce()
    elif shape == "chain":
        push()
        for _ in range(nums - 1):
            push(); reduce()
    else:
        left = nums
        while left or len(st) > 1:
            if left and (len(st) < 2 or rng.random() < 0.5):
                push(); left -= 1
            else:
                reduce()
    return toks
def small(rng):
    return {"tokens": make(rng, rng.randint(1, 5), lo=-9, hi=9)}
def build(rng, n, shape="random", ops="+-*/"):
    return {"tokens": make(rng, (n + 1) // 2, shape, ops=ops)}
