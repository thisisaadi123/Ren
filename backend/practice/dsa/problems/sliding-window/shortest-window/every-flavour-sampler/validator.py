def validate(jars):
    assert isinstance(jars, list) and 1 <= len(jars) <= 100_000, "1 <= jars.length <= 10^5"
    assert all(type(v) is int and 1 <= v <= 10**9 for v in jars), "1 <= jars[i] <= 10^9"
