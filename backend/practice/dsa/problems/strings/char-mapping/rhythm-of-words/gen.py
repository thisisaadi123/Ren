import string
def vocab(rng, size, wlen):
    out = set()
    while len(out) < size:
        out.add("".join(rng.choice("abcdefgh") for _ in range(rng.randint(1, wlen))))
    return sorted(out)
def make(rng, n, k, wlen, shape):
    letters = string.ascii_lowercase[:k]
    pattern = "".join(rng.choice(letters) for _ in range(n))
    used = sorted(set(pattern))
    pool = vocab(rng, len(used) + 3, wlen)
    rng.shuffle(pool)
    to_word = dict(zip(used, pool))
    words = [to_word[c] for c in pattern]
    if shape == "swap-word" and len(used) > 1:
        i = rng.randrange(n)
        words[i] = rng.choice([w for w in to_word.values() if w != words[i]])
    elif shape == "new-word":
        i = rng.randrange(n)
        words[i] = pool[-1]
    elif shape == "merge" and len(used) > 1:
        a, b = rng.sample(used, 2)
        words = [to_word[a] if c == b else to_word[c] for c in pattern]
    elif shape == "length":
        if rng.random() < 0.5 or n == 1:
            words.append(rng.choice(words))
        else:
            words.pop()
    return {"pattern": pattern, "sentence": " ".join(words)}
def small(rng):
    return make(rng, rng.randint(1, 5), rng.randint(1, 3), 3, rng.choice(["ok", "ok", "swap-word", "new-word", "merge", "length"]))
def build(rng, n, k=26, wlen=8, shape="ok"):
    return make(rng, n, k, wlen, shape)
