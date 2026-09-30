from ren_gen import ints
def small(rng):
    return {"nums": ints(rng, rng.randint(1, 8), -3, 3), "target": rng.randint(-4, 4)}
def build(rng, n, lo=-1000, hi=1000, target=None):
    nums = ints(rng, n, lo, hi)
    if target is None:
        i = rng.randrange(n); j = rng.randint(i, min(n - 1, i + 50))
        target = sum(nums[i : j + 1])
    return {"nums": nums, "target": max(-10**7, min(10**7, target))}
