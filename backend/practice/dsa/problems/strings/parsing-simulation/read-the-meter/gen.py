import string
JUNK = string.ascii_letters + " +-_."
def number(rng, digits, sep):
    out = []
    for k in range(digits):
        out.append(rng.choice("0123456789"))
        if k < digits - 1 and rng.random() < sep:
            out.append("_" * rng.choice([1, 1, 1, 2]))
    return "".join(out)
def make(rng, n, digits, sep, noise):
    s = " " * rng.choice([0, 0, 1, 3])
    r = rng.random()
    if r < 0.6:
        s += rng.choice("+-")
    elif r < 0.7:
        s += rng.choice(["+-", "-+", "- ", "_", "a"])
    s += number(rng, digits, sep)
    if rng.random() < 0.5:
        s += "".join(rng.choice(JUNK + "0123456789") for _ in range(noise))
    return s[:n]
def small(rng):
    if rng.random() < 0.15:
        return {"text": "".join(rng.choice(" +-_0123456789a.") for _ in range(rng.randint(0, 10)))}
    return {"text": make(rng, 30, rng.randint(0, 12), 0.3, rng.randint(0, 4))}
def build(rng, n=200, digits=10, sep=0.2, noise=5, shape="random"):
    if shape == "zeros":
        body = "0" * (digits - 4) + number(rng, 4, 0)
        return {"text": (rng.choice(["", "-", "+"]) + body)[:n]}
    if shape == "grouped":
        v = rng.randint(0, 2**32)
        g = "{:,}".format(v).replace(",", "_")
        return {"text": (" " * rng.randint(0, 3) + rng.choice(["", "-", "+"]) + g + rng.choice(["", " kWh", "_", ".5"]))[:n]}
    return {"text": make(rng, n, digits, sep, noise)}
