def validate(factors, cap):
    assert isinstance(factors, list) and 1 <= len(factors) <= 100_000, "1 <= factors.length <= 10^5"
    assert all(type(v) is int and 1 <= v <= 1000 for v in factors), "1 <= factors[i] <= 1000"
    assert type(cap) is int and 0 <= cap <= 10**6, "0 <= cap <= 10^6"
