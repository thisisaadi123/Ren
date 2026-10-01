def validate(s, k):
    assert type(s) is str and 1 <= len(s) <= 100_000, "1 <= s.length <= 10^5"
    assert all("A" <= c <= "Z" for c in s), "uppercase letters only"
    assert type(k) is int and 0 <= k <= len(s), "0 <= k <= s.length"
