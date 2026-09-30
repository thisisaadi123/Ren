from ren_gen import word
import string
ALL = string.ascii_letters + string.digits
def small(rng):
    return {"s": word(rng, rng.randint(1, 9), rng.choice(["ab", "aAb1", "xyz"]))}
def build(rng, n, alphabet="all"):
    return {"s": word(rng, n, ALL if alphabet == "all" else alphabet)}
