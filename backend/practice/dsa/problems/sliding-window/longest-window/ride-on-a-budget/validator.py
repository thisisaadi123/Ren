def validate(fares, budget):
    assert isinstance(fares, list) and 1 <= len(fares) <= 100_000, "1 <= fares.length <= 10^5"
    assert all(type(v) is int and 1 <= v <= 10**4 for v in fares), "1 <= fares[i] <= 10^4"
    assert type(budget) is int and 0 <= budget <= 10**9, "0 <= budget <= 10^9"
