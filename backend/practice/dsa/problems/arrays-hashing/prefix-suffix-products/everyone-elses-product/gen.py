def small(rng):
    return {"nums": [rng.randint(-2, 2) for _ in range(rng.randint(2, 7))]}
def build(rng, n, twos=20, zeros=0):
    nums = [rng.choice([1, -1]) for _ in range(n)]
    for i in rng.sample(range(n), min(n, twos)):
        nums[i] = rng.choice([2, -2])
    free = [i for i in range(n) if abs(nums[i]) != 2]
    for i in rng.sample(free, min(len(free), zeros)):
        nums[i] = 0
    return {"nums": nums}
