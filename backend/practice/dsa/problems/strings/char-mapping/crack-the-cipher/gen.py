import string
L = string.ascii_lowercase
def sentence(rng, n, letters, spaces=0.15):
    return "".join(" " if rng.random() < spaces else rng.choice(letters) for _ in range(n))
def make(rng, n, mlen, k, mode, spaces=0.15):
    perm = list(L)
    rng.shuffle(perm)
    enc = dict(zip(L, perm))
    enc[" "] = " "
    letters = rng.sample(L, k)
    if n >= k:
        chars = list(sentence(rng, n - k, letters, spaces)) + letters
        rng.shuffle(chars)
        plain = "".join(chars)
    else:
        plain = sentence(rng, n, letters, spaces)
    if not plain.strip():
        plain = letters[0] + plain[1:]
    if mode == "late":
        body = sentence(rng, n - k, letters[:1], 0)
        plain = body + "".join(letters)
    coded = "".join(enc[c] for c in plain)
    if mode == "known":
        msg = "".join(enc[c] for c in sentence(rng, mlen, sorted(set(plain) - {" "}) or ["a"], spaces))
    elif mode == "unknown":
        rest = [c for c in L if c not in set(coded)] or list(L)
        msg = sentence(rng, mlen, rest, spaces)
    else:
        msg = sentence(rng, mlen, L, spaces)
    if not msg:
        msg = "a"
    return {"plain": plain, "coded": coded, "message": msg}
def small(rng):
    k = rng.choice([1, 2, 3, 24, 25, 26])
    if k >= 24:
        return make(rng, k, rng.randint(1, 5), k, rng.choice(["any", "known"]), 0)
    return make(rng, rng.randint(1, 8), rng.randint(1, 8), k, rng.choice(["any", "known", "unknown"]))
def build(rng, n, mlen, k=26, mode="any", spaces=0.15):
    return make(rng, n, mlen, k, mode, spaces)
