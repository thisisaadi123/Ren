def validate(boulders):
    assert isinstance(boulders, list) and 1 <= len(boulders) <= 10**5, "1 <= boulders.length <= 10^5"
    assert all(type(w) is int and 1 <= w <= 10**9 for w in boulders), "1 <= boulders[i] <= 10^9"
