PRINTABLE = "".join(chr(c) for c in range(32, 127))
def pack(strs):
    return "".join("%d#%s" % (len(s), s) for s in strs)
def small(rng):
    strs = ["".join(rng.choice("ab#12") for _ in range(rng.choice([0, 1, 2, 3, 11]))) for _ in range(rng.randint(0, 4))]
    return {"bundle": pack(strs)}
def build(rng, count, maxlen, alpha="ab#12 ", shape="random"):
    if shape == "printable":
        alpha = PRINTABLE
    strs = ["".join(rng.choice(alpha) for _ in range(rng.randint(0, maxlen))) for _ in range(count)]
    while len(pack(strs)) > 10**5:
        strs.pop()
    return {"bundle": pack(strs)}
