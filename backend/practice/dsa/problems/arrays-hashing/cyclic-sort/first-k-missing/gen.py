from ren_gen import ints
def small(rng):
    return {"nums": ints(rng, rng.randint(1, 8), -3, 10), "k": rng.randint(1, 6)}
def build(rng, n, k=10, lo=-5, hi=None, shape="random"):
    hi = hi if hi is not None else n + 20
    if shape == "perm":
        nums = list(range(1, n + 1))
        rng.shuffle(nums)
    else:
        nums = ints(rng, n, lo, hi)
    return {"nums": nums, "k": k}
