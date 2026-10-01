def build(rng, n, shape="valid"):
    washed = rng.sample(range(10**9), n)
    if shape == "valid" or shape == "near":
        stack, served, i = [], [], 0
        while len(served) < n:
            if i < n and (not stack or rng.random() < 0.5):
                stack.append(washed[i])
                i += 1
            else:
                served.append(stack.pop())
        if shape == "near" and n >= 2:
            a = rng.randrange(n - 1)
            served[a], served[a + 1] = served[a + 1], served[a]
        return {"washed": washed, "served": served}
    if shape == "reverse":
        return {"washed": washed, "served": washed[::-1]}
    served = washed[:]
    rng.shuffle(served)
    return {"washed": washed, "served": served}


def small(rng):
    return build(rng, rng.randint(1, 6), rng.choice(("valid", "near", "random")))
