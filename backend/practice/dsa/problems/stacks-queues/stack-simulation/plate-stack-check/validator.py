def validate(washed, served):
    assert isinstance(washed, list) and 1 <= len(washed) <= 100_000, "1 <= washed.length <= 10^5"
    assert all(type(v) is int and 0 <= v <= 10**9 for v in washed), "0 <= washed[i] <= 10^9"
    assert len(set(washed)) == len(washed), "plates are distinct"
    assert isinstance(served, list) and sorted(served) == sorted(washed), "served is a rearrangement of washed"
