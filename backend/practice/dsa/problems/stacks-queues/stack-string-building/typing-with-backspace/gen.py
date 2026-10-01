from ren_gen import word


def build(rng, n, alpha="ab#", same=0):
    a = word(rng, n * 5 // 8 if same else n, alpha) or alpha[0]
    if same:
        # Type the same text with different mistakes.
        out = []
        for c in a:
            if c != "#" and rng.random() < 0.3:
                out += [rng.choice("xyz"), "#"]
            out.append(c)
        return {"a": a, "b": "".join(out)[:n]}
    return {"a": a, "b": word(rng, n, alpha)}


def small(rng):
    return build(rng, rng.randint(1, 6), rng.choice(("a#", "ab#")), rng.choice((0, 1)))
