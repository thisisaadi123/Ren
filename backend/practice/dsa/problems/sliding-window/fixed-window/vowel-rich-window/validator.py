def validate(s, k):
    assert type(s) is str and 1 <= len(s) <= 100_000, "1 <= s.length <= 10^5"
    assert all("a" <= c <= "z" for c in s), "lowercase letters only"
    assert type(k) is int and 1 <= k <= len(s), "1 <= k <= s.length"
